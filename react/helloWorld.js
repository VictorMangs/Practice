function MyButton() {
    return (
        <button>I'm a button</button>
    );
}

function AboutPage(){
    return (
        <>
            <h1>About</h1>
            <p>Hello there user! <br>How do you do?</br></p>
        </>
    );
}

// Export default keywords specify the main component in a file
// References:
//      https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export 
//      https://javascript.info/import-export
export default function MyApp(){ 
    return (
        <div>
            <h1>Welcome to my first react app!</h1>
            <MyButton /> {/* Capital letters are react components! */}
        </div>
    );
}

