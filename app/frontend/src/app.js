const API_URL = "/api/users";

const form = document.getElementById("user-form");
const formTitle = document.getElementById("form-title");
const submitBtn = document.getElementById("submit-btn");
const cancelBtn = document.getElementById("cancel-btn");
const tbody = document.getElementById("users-tbody");
const emptyState = document.getElementById("empty-state");
const messageEl = document.getElementById("message");
const refreshBtn = document.getElementById("refresh-btn");

let editingId = null;

// ---------- Helpers ----------
function showMessage(text, type = "success") {
	messageEl.textContent = text;
	messageEl.className = `message ${type}`;
	setTimeout(() => messageEl.classList.add("hidden"), 3500);
}

function resetForm() {
	form.reset();
	document.getElementById("user-id").value = "";
	editingId = null;
	formTitle.textContent = "Add New User";
	submitBtn.textContent = "Add User";
	cancelBtn.classList.add("hidden");
}

// ---------- API Calls ----------
async function fetchUsers() {
	try {
		const res = await fetch(API_URL);
		if (!res.ok) throw new Error("Failed to load users");
		const users = await res.json();
		renderUsers(users);
	} catch (err) {
		showMessage(err.message, "error");
		renderUsers([]);
	}
}

async function createUser(data) {
	const res = await fetch(API_URL, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	});
	const body = await res.json();
	if (!res.ok) throw new Error(body.error || "Failed to create user");
	return body;
}

async function updateUser(id, data) {
	const res = await fetch(`${API_URL}/${id}`, {
		method: "PUT",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	});
	const body = await res.json();
	if (!res.ok) throw new Error(body.error || "Failed to update user");
	return body;
}

async function deleteUser(id) {
	const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
	const body = await res.json();
	if (!res.ok) throw new Error(body.error || "Failed to delete user");
	return body;
}

// ---------- Render ----------
function addCell(tr, text) {
	const td = document.createElement("td");
	td.textContent = text;
	tr.appendChild(td);
}

function makeButton(label, className, onClick) {
	const btn = document.createElement("button");
	btn.className = `btn ${className}`;
	btn.textContent = label;
	btn.addEventListener("click", onClick);
	return btn;
}

function renderUsers(users) {
	tbody.replaceChildren();

	if (!users.length) {
		emptyState.classList.remove("hidden");
		return;
	}

	emptyState.classList.add("hidden");

	users.forEach((user) => {
		const tr = document.createElement("tr");
		addCell(tr, user.id);
		addCell(tr, user.first_name);
		addCell(tr, user.last_name);
		addCell(tr, user.age);
		addCell(tr, user.email);

		const actions = document.createElement("td");
		actions.appendChild(makeButton("Edit", "btn-edit", () => startEdit(user.id, users)));
		actions.appendChild(makeButton("Delete", "btn-danger", () => handleDelete(user.id)));
		tr.appendChild(actions);

		tbody.appendChild(tr);
	});
}

function startEdit(id, users) {
	const user = users.find((u) => u.id === id);
	if (!user) return;

	editingId = id;
	document.getElementById("user-id").value = id;
	document.getElementById("first_name").value = user.first_name;
	document.getElementById("last_name").value = user.last_name;
	document.getElementById("age").value = user.age;
	document.getElementById("email").value = user.email;

	formTitle.textContent = "Edit User";
	submitBtn.textContent = "Update User";
	cancelBtn.classList.remove("hidden");

	window.scrollTo({ top: 0, behavior: "smooth" });
}

async function handleDelete(id) {
	if (!confirm("Are you sure you want to delete this user?")) return;

	try {
		await deleteUser(id);
		showMessage("User deleted successfully");
		fetchUsers();
	} catch (err) {
		showMessage(err.message, "error");
	}
}

// ---------- Form Submit ----------
form.addEventListener("submit", async (e) => {
	e.preventDefault();

	const data = {
		first_name: document.getElementById("first_name").value.trim(),
		last_name: document.getElementById("last_name").value.trim(),
		age: Number(document.getElementById("age").value),
		email: document.getElementById("email").value.trim(),
	};

	try {
		if (editingId) {
			await updateUser(editingId, data);
			showMessage("User updated successfully");
		} else {
			await createUser(data);
			showMessage("User created successfully");
		}
		resetForm();
		fetchUsers();
	} catch (err) {
		showMessage(err.message, "error");
	}
});

cancelBtn.addEventListener("click", resetForm);
refreshBtn.addEventListener("click", fetchUsers);

// ---------- Init ----------
fetchUsers();
