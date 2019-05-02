package index

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path"
	"strconv"
	"strings"

	"github.com/aadhyatm/jaincatalogue/config"
)

/*
This package creates the index of Jain Siddhant Praveshika. The format is as follows:
	* question number
	* question
	* answer
	* words that the question can be searched on
	* words in the answer that can be cross searched in a question

This package will return the question/answer(s) in above format given a search word.
*/

var trie = newTrie()

// Index index struct
type Index struct {
	number        int
	chapter       int
	question      string
	answer        string
	questionWords []string
	answerWords   []string
}

func (index *Index) toString() string {
	return fmt.Sprintf("%d-%d:: q: %s, question_words: %s",
		index.chapter, index.number, index.question, index.questionWords)
}

// Contains a map of the question number to the Index
var questionAnswerMap = make(map[int]*Index) // can be created as a slice/array

// Contains the list of all Q&A
type questionAnswerList []*Index

// englishToHindiMap mapping of english words to their hindi counterpart
var englishToHindiMap = make(map[string]string)

// Map: for every word, hold the questionAnswerIndex as a list
var wordQuestionAnswerMap = make(map[string]questionAnswerList)

func createQuestionAnswerMap(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// each line is a list of 4 or 5 entires.
		// - question number
		// - chaptner number
		// - question
		// - answer
		// - words for question search
		// - words for answer search
		index := buildIndex(scanner.Text())
		questionAnswerMap[index.number] = index

		// For this index, populate wordQuestionAnswerMap
		addToWordQuestionAnswerMap(index)
	}
}

func addToWordQuestionAnswerMap(index *Index) {
	words := index.questionWords
	for _, word := range words {
		list, err := wordQuestionAnswerMap[word]
		if !err {
			list = questionAnswerList{}
		}
		list = append(list, index)
		wordQuestionAnswerMap[word] = list
	}
}

func buildIndex(line string) *Index {
	s := strings.Split(line, "#")
	chapter, err := strconv.Atoi(s[0])
	if err != nil {
		log.Fatal(err)
	}
	num, err := strconv.Atoi(s[1])
	if err != nil {
		log.Fatal(err)
	}
	question := s[2]
	answer := s[3]
	qWordsList := s[4]
	qWords := strings.Split(qWordsList, ",")

	aWordsList := ""
	var aWords []string
	if len(s) == 6 {
		aWordsList = s[4]
		aWords = strings.Split(aWordsList, ",")
	}
	return &Index{
		number: num, chapter: chapter, question: question, answer: answer,
		questionWords: qWords, answerWords: aWords,
	}
}

// GetIndexedWords blah
func GetIndexedWords() []string {
	ret := []string{}
	for word := range wordQuestionAnswerMap {
		ret = append(ret, word)
	}
	return ret
}

// InitIndex init funcction
func InitIndex() {
	cfg := config.GetConfig()

	questionAnswerFile := path.Join(cfg.DataDir, "JainPraveshika.txt")
	createQuestionAnswerMap(questionAnswerFile)

	wordsFile := path.Join(cfg.DataDir, "words_index.txt")

	// Load english words
	file, err := os.Open(wordsFile)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		splt := strings.Split(line, ",")
		hindi := splt[0]
		english := splt[1]
		englishToHindiMap[english] = hindi

		// Add both english and hindi word to trie
		trie.AddToTrie(hindi, nil)
		trie.AddToTrie(english, nil)
	}
}

// SearchResult searchresults
type SearchResult struct {
	Chapter  int
	Number   int
	Question string
	Answer   string
}

// SearchResults Search results
type SearchResults struct {
	Query   string
	Results []*SearchResult
}

// Search function
func Search(word string) SearchResults {
	indexList, ok := wordQuestionAnswerMap[word]
	if !ok {
		// search the english map
		hindi, ok1 := englishToHindiMap[word]
		if !ok1 {
			return SearchResults{}
		}
		word = hindi
		indexList, ok = wordQuestionAnswerMap[word]
		if !ok {
			return SearchResults{}
		}
	}
	results := []*SearchResult{}
	for _, index := range indexList {
		results = append(results, &SearchResult{
			Number: index.number, Question: index.question,
			Answer: index.answer, Chapter: index.chapter})
	}
	return SearchResults{Query: word, Results: results}
}

// PrefixSearch Return all results matching a prefix
func PrefixSearch(prefix string) []string {
	return trie.Search(prefix)
}

// GetEnglishWords blah
func GetEnglishWords() []string {
	words := []string{}
	for word := range englishToHindiMap {
		words = append(words, word)
	}
	return words
}
