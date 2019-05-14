package main

/*

WHAT DOES THE SCRIPT DO?
========================

The script creates the ".meta" files. These ".meta" files will be used to load
the catalogue index and help in searching. Each ".meta" file contains the JSON
form of the protobuf catalogue.Item.


HOW TO USE THIS SCRIPT
======================
The metadata of the catalogue is loaded in the following way:

  * get the base directory which contains the items
  * specify the final location where metadata files will be created
  * run the function copyDirStructure(). This function copies all the directories
	from source to destination. It also create ".meta" files for all the directories
	and marks them as a "series". Now manually go through all the ".meta" files for
	directories and remove the ones which are not a "series".
  * Now run the function createMetaFiles(). This will create ".meta" files for all the
	individual files. This also loads the "series" ID of files which are part of the series
  * Finally run the function addItemInSeries(). This will populate the "items" field of each
	series ".meta" file.

You are all set! Now manually update the "tags", "author" files etc. for each .meta file.

*/

import (
	"bytes"
	"encoding/json"
	"fmt"
	"hash/crc64"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/aadhyatm/jaincatalogue/catalogue"
	"github.com/golang/protobuf/jsonpb"
)

var baseDir = "/Users/aadhyatm/Aadhyatm Drive/"
var metadataBaseDir = path.Join(os.Getenv("GOPATH"), "src/github.com/aadhyatm/jaincatalogue/data/catalogue/")

// http://golang.org/pkg/hash/crc64/#pkg-constants
var crcTable = crc64.MakeTable(crc64.ISO)

func getUUID(s string) uint64 {
	checksum64 := crc64.Checksum([]byte(s), crcTable)
	return checksum64
}

func writeItemToFile(item *catalogue.Item, filename string) {
	m := jsonpb.Marshaler{
		EmitDefaults: true,
		OrigName:     true,
	}
	j, _ := m.MarshalToString(item)
	finalJSON := prettyPrint(j)

	f, err := os.Create(filename)

	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	defer f.Close()

	_, err1 := f.WriteString(finalJSON)

	if err1 != nil {
		panic(err1)
	}
}

func prettyPrint(in string) string {
	var out bytes.Buffer
	err := json.Indent(&out, []byte(in), "", "\t")
	if err != nil {
		return in
	}
	return out.String()
}

func getFileType(s string) catalogue.Item_Type {
	ext := strings.ToLower(filepath.Ext(s))

	if ext == ".mp3" {
		return catalogue.Item_AUDIO
	}
	if ext == ".pdf" {
		return catalogue.Item_TEXT
	}
	if ext == ".mp4" || ext == ".mov" || ext == ".dat" || ext == ".mpeg" {
		return catalogue.Item_VIDEO
	}
	if ext == ".jpg" || ext == ".jpeg" || ext == ".png" {
		return catalogue.Item_IMAGE
	}

	return catalogue.Item_OTHER
}

func getItemFromFile(fname string) *catalogue.Item {
	_, err := os.Stat(fname)
	if err != nil {
		return nil
	}

	_, err = os.Open(fname)
	if err != nil {
		return nil
	}

	contents, _ := ioutil.ReadFile(fname)
	c := catalogue.Item{}
	err1 := jsonpb.UnmarshalString(string(contents), &c)
	if err1 != nil {
		panic(err1)
	}

	return &c
}

func getSeriesID(s string) uint64 {
	dirPath := filepath.Dir(s)
	metaFile := dirPath + ".meta"
	_, err := os.Stat(metaFile)

	if err != nil {
		// meta file does not exist. File is not a series
		return 0
	}

	// Files exists. Read it and return value
	c := getItemFromFile(metaFile)
	return c.Uuid
}

// If a string is of the form "<number> ... ", it strips the number
func cleanUp(s string) string {
	split := strings.Split(s, " ")
	_, err := strconv.Atoi(split[0])
	if err == nil {
		// num is number. skip it
		split = split[1:]
		if split[0] == "-" {
			split = split[1:]
		}
		final := strings.Join(split, " ")
		fmt.Printf("Cleaned up %s to %s\n", s, final)
		return final
	}
	return s
}

func createMetaFile(filePath string) {
	// fmt.Println("Creating meta file for ", filePath)
	// Series ID
	id := getSeriesID(filePath)
	t := getFileType(filePath)

	relativePath, _ := filepath.Rel(metadataBaseDir, filePath)

	name := path.Base(filePath)
	if strings.Contains(relativePath, "Bhakti") {
		name = cleanUp(name)
	}

	name = strings.TrimSuffix(name, filepath.Ext(name))

	// Create proto
	c := catalogue.Item{
		Name:             name,
		Author:           "",
		Path:             relativePath,
		Uuid:             getUUID(relativePath),
		OriginalAuthor:   "",
		Type:             t,
		Tags:             make([]string, 0),
		ShortDescription: "",
		Description:      "",
		LocationUrl:      "",
		ThumbnailUrl:     "",
		Series:           false,
	}
	if id > 0 {
		c.SeriesUuid = id
	}

	metaFileName := filePath + ".meta"
	writeItemToFile(&c, metaFileName)
}

func createMetaFiles(baseDir string, metadataDir string) {
	err := filepath.Walk(baseDir, func(p string, info os.FileInfo, err error) error {
		if info.IsDir() {
			return nil
		}
		if p[0:1] == "." {
			// hidden file. skip
			fmt.Println("Skipping hidden file ", p)
			return nil
		}
		if path.Base(p)[0:4] == "Icon" {
			// Icon file. Skip
			fmt.Println("Skipping Icon file ", p)
			return nil
		}
		if filepath.Ext(p) == ".meta" {
			// Do not touch meta files
			return nil
		}
		relPath, _ := filepath.Rel(baseDir, p)
		fullPath := path.Join(metadataDir, relPath)

		// Do not create metaFile if the directory doesn't exist
		dir := path.Dir(fullPath)
		_, err1 := os.Stat(dir)
		if err1 != nil {
			return nil
		}

		// Initialize and create the metadata file
		createMetaFile(fullPath)
		return nil
	})

	if err != nil {
		panic(err)
	}
}

func copyDirStructure(baseDir string, metadataDir string) {
	err := filepath.Walk(baseDir, func(p string, info os.FileInfo, err error) error {
		if !info.IsDir() {
			return nil
		}
		if p[0:1] == "." {
			// hidden file. skip
			fmt.Println("Skipping dir ", p)
			return nil
		}
		relativePath, _ := filepath.Rel(baseDir, p)

		// Initialize and create the metadata file
		createDirMetaFile(relativePath)
		fmt.Println()
		return nil
	})

	if err != nil {
		panic(err)
	}
}

func createDirMetaFile(relativePath string) {
	dirName := path.Join(metadataBaseDir, relativePath)

	name := path.Base(dirName)
	if strings.Contains(relativePath, "Bhakti") {
		name = cleanUp(name)
	}

	// Create proto
	c := catalogue.Item{
		Name:             name,
		Author:           "",
		Path:             relativePath,
		Uuid:             getUUID(relativePath),
		OriginalAuthor:   "",
		Type:             catalogue.Item_SERIES,
		Tags:             make([]string, 0),
		ShortDescription: "",
		Description:      "",
		LocationUrl:      "",
		ThumbnailUrl:     "",
		Series:           true,
		Items:            make([]uint64, 0),
	}

	fileName := dirName + ".meta"
	fmt.Println("Creating directory: ", dirName)
	// Write to meta file and create the directory
	err2 := os.MkdirAll(dirName, 0755)
	if err2 != nil {
		fmt.Print(err2)
		panic(err2)
	}

	fmt.Println("Creating meta file: ", fileName)
	writeItemToFile(&c, fileName)
}

func addItemsInSeries(metadataDir string) {
	err := filepath.Walk(metadataDir, func(p string, info os.FileInfo, err error) error {
		if filepath.Ext(p) != ".meta" {
			return nil
		}

		// read the meta file
		c := getItemFromFile(p)
		if !c.Series {
			return nil
		}

		// This is a series. Get all the items in the series
		dir := path.Join(metadataBaseDir, c.Path)
		fmt.Println("Found series ", dir)

		// Get all files inside the directory
		files, err1 := ioutil.ReadDir(dir)
		if err1 != nil {
			panic(err)
		}

		for _, f := range files {
			if f.IsDir() {
				continue
			}

			if filepath.Ext(f.Name()) != ".meta" {
				continue
			}
			fullName := filepath.Join(dir, f.Name())
			seriesItem := getItemFromFile(fullName)
			c.Items = append(c.Items, seriesItem.Uuid)
		}

		// Write item back to file
		writeItemToFile(c, p)
		return nil
	})

	if err != nil {
		panic(err)
	}
}

func main() {
	// createMetaFiles(baseDir, metadataBaseDir)
	// copyDirStructure(baseDir, metadataBaseDir)
	addItemsInSeries(metadataBaseDir)
}
