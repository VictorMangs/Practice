// Initialize user
const user = {
    name: "Messi Roman",
    imageUrl: "https://i.imgur.com/yXOvdOSs.jpg",
    imageSize: 90,
}

// Create main function called Profile
export default function Profile(){
    return (
        <>
            <h1>{user.name}</h1>
            <img
                className="avatar"
                src={user.imageUrl}
                alt={'Photo of '+ user.name}
                style={{
                    width: user.imageSize,
                    height: user.imageSize
                }}
            />
        </>
    );
}
