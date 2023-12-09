let content;

// Three modes of if statements
if (isLoggedIn){
    content = <h1>Logged in!</h1>
} else{
    content = <h1>Not logged in</h1>
}
return(
    <div>
        {content}
    </div>
);


// Using conditional "?" operator
{/* <div>
    {isLoggedIn ? (
        <h1>Logged in!</h1>
    ) : (
        <h1>Not logged in</h1>
    )

    }
</div> */}


// Use logical && if else isn't needed
{/* <div>
    {isLoggedIn && <h1>Logged in!</h1>}
</div> */}
