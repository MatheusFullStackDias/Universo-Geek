# 🌌 Universo Geek — Pinterest thematic clone

An application designed for the anime community to share their favorite arts and wallpapers. This project features user authentication, media upload management, dynamic profiles, and access control rules to simulate a secure social network.

---

## 🚀 Main Features

* **Secure Authentication:** Complete registration and login system utilizing Flask-Login and password hashing for data protection.
* **Dynamic Feed:** A collective wall that queries and displays all uploaded media chronologically, allowing exploration of content from other users.
* **Media Upload & Management:** Implementation of a secure upload pipeline where users can upload, view in full screen, and delete their own posts.
* **Dynamic Profiles:** Customizable profile area where clicking the avatar opens a hidden upload flow to update the profile picture instantly.
* **Strict Access Control (Security):** Back-end validation preventing unauthorized users from deleting other users' posts or modifying foreign profile pictures.
* **Smart UI Enquaderment:** Front-end optimization using CSS `object-position` to automatically focus and crop images on faces/characters.

---

## 🛠️ Technologies & Tools

This project showcases a modern Full-Stack architecture separating presentation logic from server-side operations:

| Layer | Technologies | Key Responsibility |
| :--- | :--- | :--- |
| **Back-End** | Python (Flask) | Architecture, routing, and business logic |
| **Database** | Flask-SQLAlchemy (SQLite) | Relational modeling, User-Post relationships |
| **Front-End** | HTML5, CSS3, JavaScript | UI, event-driven state changes (DOM manipulation) |
| **Security** | Werkzeug, Flask-Login | Hashing, route shielding (`@login_required`) |

---

## 📐 Architecture & Database Model

The database is built on a relational pattern with strict cascade deleting constraints:

* **User Model:** Stores credentials, secure password hashes, and user metadata. One-to-Many relationship with the Post Model.
* **Post Model:** Stores unique media tracking names, time stamps, and maintains a Foreign Key (`id_usuario`) referencing the owner.

---

## 💻 Visual Engineering (UX/UI Highlights)

### ⚡ Dynamic Form State Change
To prevent generic browser elements from breaking the interface design, the standard file picker was hidden. A custom `<label>` acts as a drop-zone container. Upon selecting a file, JavaScript captures the DOM event, shifts the UI border to a green success state, updates the file string name, and activates the submission action with a vivid state transition on the saving button.

### 🔄 The PRG Pattern (Post/Redirect/Get)
Implemented the PRG pattern across uploading routers. After a successful database commit, the server forces a client-side redirect instead of serving a static template. This pattern neutralizes duplicate form submission bugs during page refreshes (`F5`).

---

## 🔧 How to Run the Project Locally

Follow these steps to set up the development environment:

1. Clone the repository:
   ```bash
   git clone [https://github.com/MatheusFullStackDias/Universo-Geek.git](https://github.com/MatheusFullStackDias/Universo-Geek.git)
   

---

## 🧑‍💻 Autor

Desenvolvido com ☕ e 💻 por **Matheus Galvão Dias** * **LinkedIn:** [in/dev-matheus-galvão-dias-624720365](https://www.linkedin.com/in/dev-matheus-galvão-dias-624720365/)
* **E-mail:** [matheusgalvaodias3@gmail.com](mailto:matheusgalvaodias3@gmail.com)
* **Portfólio/GitHub:** [github.com/MatheusFullStackDias](https://github.com/MatheusFullStackDias)