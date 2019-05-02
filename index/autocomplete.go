package index

import (
	"fmt"
	"strings"

	"github.com/golang-collections/collections/stack"
)

/*
	Articles to read: https://blog.golang.org/strings
	Unicode: https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
	Unicode website: https://www.unicode.org/charts/PDF/U0900.pdf
	Trie with rune: https://github.com/derekparker/trie/blob/master/trie.go
*/

// trieNode Defines the data structure for the Trie
type trieNode struct {
	val        rune               // the character value stored by this TrieNode
	term       bool               // whether the ndoe represents end of a word
	depth      int                // height of the trie at this node
	parent     *trieNode          // parent pointer
	children   map[rune]*trieNode // children TrieNodes
	fullString []rune             // The entire string that is added till here
	meta       interface{}        // the value associated with the trie
}

func newTrieNode(v rune) *trieNode {
	return &trieNode{val: v, term: false, depth: 0, children: make(map[rune]*trieNode)}
}

func (t *trieNode) toString() string {
	var str strings.Builder
	str.WriteString("val: ")
	str.WriteRune(t.val)
	str.WriteString(" term: ")
	str.WriteString(fmt.Sprint(t.term))
	str.WriteString(" fullString: ")
	str.WriteString(string(t.fullString))

	return str.String()
}

// Trie trie data structure
type Trie struct {
	Root *trieNode
}

// newTrie Creates a new trie with empty root node
func newTrie() *Trie {
	return &Trie{
		Root: &trieNode{children: make(map[rune]*trieNode), depth: 0, term: false, val: 0},
	}
}

// ToString Prints the entire trie
func (t *Trie) ToString() string {
	var str strings.Builder
	st := stack.New()
	root := t.Root
	st.Push(root)
	for {
		if st.Len() == 0 {
			break
		}
		node := st.Pop().(*trieNode)
		str.WriteString(node.toString())
		str.WriteString("\n")

		// Add all the children of 'node' to stack
		for _, v := range node.children {
			st.Push(v)
		}
	}
	return str.String()
}

// AddToTrie Adds a word to the trie
func (t *Trie) AddToTrie(word string, meta interface{}) {
	runes := []rune(word)

	node := t.Root

	currRunes := make([]rune, 0)
	for _, rune := range runes {
		currRunes = append(currRunes, rune)
		trieNode, ok := node.children[rune]
		if !ok {
			// add a new TrieNode
			trieNode = newTrieNode(rune)
			trieNode.fullString = currRunes
			trieNode.meta = meta
			node.children[rune] = trieNode
		}
		node = trieNode
	}
	node.term = true
}

// getFromTrie Finds whether a word exists in the trie. Returns nil if it doesn't
func (t *Trie) getFromTrie(word string, ignoreTerm bool) *trieNode {
	runes := []rune(word)

	node := t.Root

	for _, rune := range runes {
		val, ok := node.children[rune]
		if !ok {
			return nil
		}
		node = val
	}
	if ignoreTerm {
		return node
	}
	if node.term {
		return node
	}
	return nil
}

// Search Return all words matching a prefix
func (t *Trie) Search(prefix string) []string {
	results := make([]string, 0)

	baseNode := t.getFromTrie(prefix, true)
	if baseNode == nil {
		return nil
	}

	// Add all the matching terminal child-nodes
	st := stack.New()
	st.Push(baseNode)
	for {
		if st.Len() == 0 {
			break
		}
		front := st.Pop().(*trieNode)
		if front.term {
			results = append(results, string(front.fullString))
		}
		for _, node := range front.children {
			st.Push(node)
		}
	}
	return results
}
