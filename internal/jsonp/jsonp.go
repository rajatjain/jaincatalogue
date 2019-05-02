package jsonp

// Copyright (C) Philip Schlump, 2013-2015.
// License in ./LICENSE file - MIT.
// Version: 1.0.0

import (
	"fmt"
	"net/http"
	"net/url"
)

//
// Example of Use
//
// In a handler you build some JSON then call JsonP on the return value.
//
//	 	func handleVersion(res http.ResponseWriter, req *http.Request) {
// 			res.Header().Set("Content-Type", "application/json")
// 			io.WriteString(res, jsonp.JsonP(fmt.Sprintf(`{"status":"success", "version":"1.0.0"}`+"\n"), res, req))
// 		}
//

// JSONPrefix prefix
var JSONPrefix string

// SetJSONPrefix Set a prefix that will be pre-pended to every return JSON string.
func SetJSONPrefix(p string) {
	JSONPrefix = p
}

// JSONP Take a string 's' in JSON and if a get parameter "callback" is specified then format this for JSONP callback.
// If it is not a JSONp call (no "callback" parameter) then add JSON_Prefix to the beginning.
func JSONP(s string, res http.ResponseWriter, req *http.Request) string {

	u, err := url.ParseRequestURI(req.RequestURI)
	if err != nil {
		return JSONPrefix + s
	}
	m, err := url.ParseQuery(u.RawQuery)
	if err != nil {
		return JSONPrefix + s
	}
	callback := m.Get("callback")
	if callback != "" {
		res.Header().Set("Content-Type", "application/javascript; charset=UTF-8")
		return fmt.Sprintf("%s(%s);", callback, s)
	} else {
		return JSONPrefix + s
	}
}

// Param If "callback" is not "" then convert the JSON string 's' to a JSONp callback.
// If it is not a JSONp call (no "callback" parameter) then add JSON_Prefix to the beginning.
func Param(s string, res http.ResponseWriter, callback string) string {
	if callback != "" {
		res.Header().Set("Content-Type", "application/javascript")
		return fmt.Sprintf("%s(%s);", callback, s)
	} else {
		return JSONPrefix + s
	}
}

// PrependPrefix For non-JSONP callable - just prepend the prefix and return.
func PrependPrefix(s string) string {
	return JSONPrefix + s
}
