from fpdf import FPDF

html_content = """
<h1>Project Documentation: FastAPI To-Do List CRUD API</h1>

<h2>1. Project Goals</h2>
<p>The primary goal of this project was to build a simple, lightweight RESTful API for managing a To-Do list using FastAPI and Python. This serves as a foundational exercise to understand API routing, HTTP methods, status codes, and data validation without the complexity of a persistent database.</p>

<h2>2. What Was Done</h2>
<ul>
  <li>Initialized a Python virtual environment and Git repository.</li>
  <li>Created a FastAPI application (main.py) with an in-memory database (tasks_db).</li>
  <li>Implemented full CRUD operations (Create, Read, Update, Delete) with appropriate status codes (200, 201, 204).</li>
  <li>Added robust error handling (400 Bad Request for invalid input, 404 Not Found for missing tasks).</li>
  <li>Implemented optional query parameters for filtering tasks by status and searching by title.</li>
  <li>Created utility endpoints for health checks (/health), statistics (/stats), and resetting the database (/reset).</li>
  <li>Simulated an "AI vs Me" code review by generating an alternative implementation (ai-version/main.py) to compare design choices.</li>
  <li>Wrote a comprehensive README.md and executed a 7-stage Git commit history.</li>
</ul>

<h2>3. Features, Uses, and "Why & How"</h2>

<h3>A. In-Memory Storage (tasks_db)</h3>
<p><b>What it is:</b> A simple Python list pre-filled with 3 default tasks.</p>
<p><b>Use/Goal:</b> To store task data temporarily while the server runs.</p>
<p><b>Why:</b> It removes the overhead of configuring SQL or NoSQL databases, making it perfect for rapid prototyping and learning.</p>
<p><b>How:</b> Stored globally as tasks_db: List[Task]. Note that due to the "Mortality Experiment", this data is wiped clean whenever the server restarts.</p>

<h3>B. Pydantic Data Models</h3>
<p><b>What it is:</b> TaskInput and Task classes inheriting from BaseModel.</p>
<p><b>Use/Goal:</b> To enforce strict data types (e.g., ensuring 'id' is an integer and 'done' is a boolean).</p>
<p><b>Why:</b> To automatically validate incoming JSON requests and format outgoing responses, preventing bad data from crashing the app.</p>
<p><b>How:</b> Passed into the endpoint functions as type hints. FastAPI automatically uses them to parse requests.</p>

<h3>C. Core CRUD Endpoints</h3>
<p><b>1. POST /tasks (Create):</b> Accepts a title. Validates it isn't empty. Calculates the next ID and appends it to the list. Returns <b>201 Created</b>.</p>
<p><b>2. GET /tasks (Read All):</b> Returns the list of tasks. Includes optional query parameters ?done=true and ?search=keyword to filter the list dynamically.</p>
<p><b>3. GET /tasks/{id} (Read One):</b> Retrieves a specific task by its URL path ID. Returns <b>404 Not Found</b> if missing.</p>
<p><b>4. PUT /tasks/{id} (Update):</b> Modifies the title and completion status of an existing task. Blocks empty titles (400 Bad Request).</p>
<p><b>5. DELETE /tasks/{id} (Delete):</b> Removes a task from the list and returns <b>204 No Content</b> to indicate successful deletion without a response body.</p>

<h3>D. Utility Endpoints</h3>
<p><b>1. GET /stats:</b> Calculates and returns the total number of tasks, completed tasks, and open tasks. Useful for dashboard metrics.</p>
<p><b>2. POST /reset:</b> Clears the current list and restores the original 3 dummy tasks. Essential for quickly restarting tests after the database gets messy.</p>

<h3>E. Interactive Documentation (Swagger UI)</h3>
<p><b>What it is:</b> An automatic webpage hosted at /docs.</p>
<p><b>Use/Goal:</b> To visually explore and interact with the API.</p>
<p><b>Why:</b> It saves developers from having to use external tools like Postman or write long terminal curl commands to test their endpoints.</p>
<p><b>How:</b> FastAPI reads the Python code, type hints, and Pydantic models to instantly generate an OpenAPI schema in the background.</p>

<p><br/><i>Generated automatically for the CRUD API Project Assignment.</i></p>
"""

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.write_html(html_content)
pdf.output("Project_Documentation.pdf")
