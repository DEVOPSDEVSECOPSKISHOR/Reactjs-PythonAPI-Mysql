import React, { useEffect, useState } from 'react';

function ItemsList() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetch('/api/tasks')
            .then(response => response.json())
            .then(data => setItems(data));
    }, []);

    return (
        <ul>
            {items.map(item => (
                <li key={item.id}><strong>{item.title}</strong>: {item.description}</li>
            ))}
        </ul>
    );
}

export default ItemsList;
