const products = [
    {title: "Cabbage", isFruit: false, id: 1},
    {title: "Garlic", isFruit: false, id: 2},
    {title: "Apple", isFruit: true, id: 3},
];

export default function ShoppingList(){
    const listItems = products.map(product =>
        <li 
        key={product.id}
            style={{
                color: product.isFruit ? "orange" : "green"
            }}
            >
            {product.title}
        </li>  
    );

    return(
        <u1>{listItems}</u1>
    );
}