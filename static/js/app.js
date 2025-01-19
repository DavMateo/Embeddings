// DOM Elements
const todoForm = document.getElementById('todo-form');
const todoTitleInput = document.getElementById('todo-title');
const todoDescriptionInput = document.getElementById('todo-description');
const todoList = document.getElementById('todo-list');
const clearCompletedBtn = document.getElementById('clear-completed');
const searchInput = document.getElementById('search-input');
const searchTypeToggle = document.getElementById('search-type-toggle');
const errorMessage = document.getElementById('error-message');

// Todo array to store tasks
let todos = JSON.parse(localStorage.getItem('todos')) || [];

// Function to save todos to local storage
function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

// Function to render todos
function renderTodos(todosToRender = todos) {
    todoList.innerHTML = '';
    todosToRender.forEach((todo, index) => {
        const li = document.createElement('li');
        li.className = 'todo-item';
        if (todo.completed) {
            li.classList.add('completed');
        }

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = todo.completed;
        checkbox.addEventListener('change', () => toggleTodo(index));

        const content = document.createElement('div');
        content.className = 'todo-content';

        const title = document.createElement('div');
        title.className = 'todo-title';
        title.textContent = todo.title;

        const description = document.createElement('div');
        description.className = 'todo-description';
        description.textContent = todo.description;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '&times;';
        deleteBtn.addEventListener('click', () => deleteTodo(index));

        content.appendChild(title);
        content.appendChild(description);
        li.appendChild(checkbox);
        li.appendChild(content);
        li.appendChild(deleteBtn);
        todoList.appendChild(li);
    });
}

// Function to add a new todo
function addTodo(title, description) {
    todos.push({ title, description, completed: false });
    saveTodos();
    renderTodos();
}

// Function to toggle todo completion status
function toggleTodo(index) {
    todos[index].completed = !todos[index].completed;
    saveTodos();
    renderTodos();
}

// Function to delete a todo
function deleteTodo(index) {
    const todoItem = todoList.children[index];
    todoItem.classList.add('deleting');
    todoItem.addEventListener('animationend', () => {
        todos.splice(index, 1);
        saveTodos();
        renderTodos();
    });
}

// Function to clear completed todos
function clearCompleted() {
    const completedItems = todoList.querySelectorAll('.completed');
    completedItems.forEach(item => {
        item.classList.add('clear-completed');
        item.addEventListener('animationend', () => {
            item.remove();
        });
    });
    todos = todos.filter(todo => !todo.completed);
    saveTodos();
}

// Function to show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('show');
    setTimeout(() => {
        errorMessage.classList.remove('show');
    }, 3000);
}

// Function to search todos
function searchTodos() {
    const searchTerm = searchInput.value.toLowerCase();
    const searchType = searchTypeToggle.checked ? 'description' : 'title';

    const filteredTodos = todos.filter(todo =>
        todo[searchType].toLowerCase().includes(searchTerm)
    );

    renderTodos(filteredTodos);
}

// Function to prepare search data for API
function prepareSearchData() {
    return {
        searchField: searchTypeToggle.checked ? 'description' : 'title',
        query: searchInput.value
    };
}

// Event Listeners
todoForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const title = todoTitleInput.value.trim();
    const description = todoDescriptionInput.value.trim();

    if (title && description) {
        addTodo(title, description);
        todoTitleInput.value = '';
        todoDescriptionInput.value = '';
    } else {
        showError('Please fill in both title and description.');
        if (!title) todoTitleInput.classList.add('input-error');
        if (!description) todoDescriptionInput.classList.add('input-error');

        setTimeout(() => {
            todoTitleInput.classList.remove('input-error');
            todoDescriptionInput.classList.remove('input-error');
        }, 500);
    }
});

clearCompletedBtn.addEventListener('click', clearCompleted);

searchInput.addEventListener('input', searchTodos);
searchTypeToggle.addEventListener('change', searchTodos);

// Remove error class on input
todoTitleInput.addEventListener('input', () => todoTitleInput.classList.remove('input-error'));
todoDescriptionInput.addEventListener('input', () => todoDescriptionInput.classList.remove('input-error'));

// Initial render
renderTodos();

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        const focusableElements = todoList.querySelectorAll('input[type="checkbox"], button');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
});

// Example of how to use the prepareSearchData function for API integration
searchInput.addEventListener('input', () => {
    const searchData = prepareSearchData();
    console.log('Search data ready for API:', searchData);
    // Here you would typically send this data to your API
});