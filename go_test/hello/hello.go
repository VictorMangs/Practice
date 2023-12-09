// ========= Hello World ========= //
package main

import (
	"fmt"

	"rsc.io/quote/v4"

	"example.com/greetings"
)

// ========= main ========= //
// main outputs text and calls other functions.
func main() {
	// Variables and such
	name := "Victorius"
	fmt.Println("Gluten Mornings to ya", name)
	
	// Print a quote
	fmt.Println(quote.Go())
	
	// Get a greeting message and print it.
    message := greetings.Hello("Gladys")
    fmt.Println(message)
}
