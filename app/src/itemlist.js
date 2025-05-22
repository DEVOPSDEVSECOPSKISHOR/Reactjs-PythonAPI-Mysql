import React, { useEffect, useState } from 'react';

function ItemsList() {
    const [items, setItems] = useState([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    // Fetch items on component mount
    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = () => {
        fetch('/api/tasks')
            .then(response => response.json())
            .then(data => setItems(data));
    };

    const handleAddItem = (e) => {
        e.preventDefault();

        const newItem = { title, description };

        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newItem),
        })
        .then(response => {
            if (response.ok) {
                setTitle('');
                setDescription('');
                fetchItems();
            } else {
                console.error('Failed to add item');
            }
        });
    };

    return (
        <div>
            <h2>Add New Item</h2>
            <form onSubmit={handleAddItem}>
                <input 
                    type="text" 
                    placeholder="Title" 
                    value={title} 
                    onChange={(e) => setTitle(e.target.value)} 
                    required
                />
                <input 
                    type="text" 
                    placeholder="Description" 
                    value={description} 
                    onChange={(e) => setDescription(e.target.value)} 
                    required
                />
                <button type="submit">Add</button>
            </form>

            <h2>Items List</h2>
            <ul>
                {items.map(item => (
                    <li key={item.id}>
                        <strong>{item.title}</strong>: {item.description}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ItemsList;
