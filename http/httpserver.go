package http

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"text/template"

	config "github.com/aadhyatm/jaincatalogue/config"
	index "github.com/aadhyatm/jaincatalogue/index"
	"github.com/aadhyatm/jaincatalogue/internal/jsonp"
	log "github.com/google/logger"
)

type oneResult struct {
	Word string
}

var templates *template.Template

func searchHandler(w http.ResponseWriter, r *http.Request) {
	log.Info("Query params: ", r.URL.Query())

	prefixWord := strings.ToLower(r.URL.Query().Get("prefix"))
	queryWord := strings.ToLower(r.URL.Query().Get("query"))
	outputFormat := r.Header.Get("Accept")
	log.Info("OutputFormat: ", outputFormat)
	returnJSON := false
	if outputFormat == "application/json" {
		log.Info("Returning Json output")
		returnJSON = true
	}

	if queryWord != "" {
		// return complete output
		results := index.Search(queryWord)
		if returnJSON {
			json, err := json.Marshal(results)
			if err != nil {
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusInternalServerError)
				w.Write([]byte(err.Error()))
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			w.Write(json)
			return
		}
		// In both question & answer, replace "\n" by "<br>"
		for _, result := range results.Results {
			result.Answer = strings.Replace(result.Answer, "\\n", "<br><br>", -1)
		}

		templates.ExecuteTemplate(w, "query", results)
	} else if prefixWord != "" {
		// return autocomplete output
		words := index.PrefixSearch(prefixWord)
		log.Info("Searching words for prefix: ", prefixWord)
		log.Info("Returning: ", words)

		oneResults := []oneResult{}
		for _, word := range words {
			one := oneResult{Word: word}
			oneResults = append(oneResults, one)
		}
		log.Info("Returning words: ", words)
		w.Header().Set("Content-Type", "application/json; charset=UTF-8")
		j, _ := json.Marshal(oneResults)
		io.WriteString(w, jsonp.JSONP(string(j), w, r))
		return
	} else {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		return
		// return nothing
	}
}

// InitHTTPServer Initializes HTTP Server
func InitHTTPServer() {
	cfg := config.GetConfig()
	log.Info("HTMLDir: ", cfg.HTMLDir)
	fs := http.FileServer(http.Dir(cfg.HTMLDir))

	templates = template.Must(template.ParseGlob(config.GetConfig().TemplateDir + "/*"))

	http.Handle("/", fs)
	http.HandleFunc("/q", searchHandler)

}

// StartHTTPServer Start HTTP Server
func StartHTTPServer() {
	cfg := config.GetConfig()
	log.Info("Starting HTTP Server at port: ", cfg.Port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", cfg.Port), nil))
}
