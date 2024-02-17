package greetings

import "fmt"

// ========= Greetings ========= //
// Hello returns a greeting for the named person.
// func function-name(variable parameter-type) return-type
// := is shortcut for decalring and initializing a variable in one line
// example
// message := "blah"
// or
// var message string
// message = "blah"
func Hello(name string) string {
    // Return a greeting that embeds the name in a message.
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    return message
}