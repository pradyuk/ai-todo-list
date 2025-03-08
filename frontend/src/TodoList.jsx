import { useState, useEffect } from "react";
import axios from "axios";
import { FaEdit, FaTrash, FaPlus, FaComments, FaEye, FaEyeSlash, FaCheckCircle, FaTimesCircle } from "react-icons/fa";
import Chatbot from "./Chatbot";

const API_URL = "/api/tasks/";
const EMPLOYEE_API_URL = "/api/employees/";
const COMMENT_API_URL = "/api/comments/";

export default function TodoList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newTask, setNewTask] = useState("");
  const [editingTask, setEditingTask] = useState(null);
  const [editText, setEditText] = useState("");
  const [humanEmployeeId, setHumanEmployeeId] = useState(null);
  const [newComment, setNewComment] = useState({});
  const [editingComment, setEditingComment] = useState({});
  const [editCommentText, setEditCommentText] = useState("");
  const [showComments, setShowComments] = useState({}); // Track which tasks have comments visible
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState("");


  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await axios.get(EMPLOYEE_API_URL);
        setEmployees(response.data);
      } catch (error) {
        console.error("Error fetching employees:", error);
      }
    };

    fetchEmployees();
  }, []);



  useEffect(() => {
    const fetchData = async () => {
      try {
        const tasksResponse = await axios.get(API_URL);
        setTasks(tasksResponse.data);

        const employeesResponse = await axios.get(EMPLOYEE_API_URL);
        const humanEmployee = employeesResponse.data.find(emp => emp.employee_type === "human");

        if (humanEmployee) {
          setHumanEmployeeId(humanEmployee.id);
        } else {
          console.error("No human employee found.");
        }

        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const toggleComments = (taskId) => {
    setShowComments((prevState) => ({
      ...prevState,
      [taskId]: !prevState[taskId], // Toggle state for each task
    }));
  };

  const handleAddTask = async () => {
    if (!newTask.trim() || !selectedEmployee) return;

    try {
      await axios.post(API_URL, {
        title: newTask,
        completed: false,
        assigned_to_id: selectedEmployee,
      });

      setNewTask("");
      setSelectedEmployee("");
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };


  const handleDeleteTask = async (taskId) => {
    try {
      await axios.delete(`${API_URL}${taskId}/`);
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  const handleEditTask = async (taskId) => {
    if (!editText.trim()) return;
    try {
      await axios.patch(`${API_URL}${taskId}/`, { title: editText });
      setEditingTask(null);
      setEditText("");
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  const handleAddComment = async (taskId) => {
    if (!newComment[taskId]?.trim()) return;
    if (!humanEmployeeId) return console.error("No human employee ID found.");
    try {
      await axios.post(COMMENT_API_URL, {
        task: taskId,
        employee_id: humanEmployeeId,
        content: newComment[taskId],
      });
      setNewComment({ ...newComment, [taskId]: "" });
    } catch (error) {
      console.error("Error adding comment:", error);
    }
  };

  const handleDeleteComment = async (commentId) => {
    try {
      await axios.delete(`${COMMENT_API_URL}${commentId}/`);
    } catch (error) {
      console.error("Error deleting comment:", error);
    }
  };

  const handleEditComment = async (commentId) => {
    if (!editCommentText.trim()) return;
    try {
      await axios.patch(`${COMMENT_API_URL}${commentId}/`, { content: editCommentText });
      setEditingComment({});
      setEditCommentText("");
    } catch (error) {
      console.error("Error updating comment:", error);
    }
  };

  if (loading) return <p>Loading tasks...</p>;

  return (
    <div style={styles.container}>
      <div style={styles.column}>
        <h2 style={styles.heading}>To-Do List</h2>

        <div style={styles.addTaskContainer}>
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="Enter new task"
            style={styles.input}
          />

          {/* Employee Drop-down */}
          <select
            value={selectedEmployee}
            onChange={(e) => setSelectedEmployee(e.target.value)}
            style={styles.select}
          >
            <option value="">Select Employee</option>
            {employees.map((employee) => (
              <option key={employee.id} value={employee.id}>
                {employee.name}
              </option>
            ))}
          </select>

          <button onClick={handleAddTask} style={styles.button}>
            <FaPlus /> Add Task
          </button>
        </div>


        <ul style={styles.taskList}>
          {tasks.map((task) => (
            <li key={task.id} style={styles.taskItem}>
              {editingTask === task.id ? (
                <>
                  <input
                    type="text"
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                    style={styles.input}
                  />
                  <button onClick={() => handleEditTask(task.id)} style={styles.button}>Save</button>
                  <button onClick={() => setEditingTask(null)} style={styles.cancelButton}>Cancel</button>
                </>
              ) : (
                <>
                  <span>
                    {task.title} [{task.assigned_to ? task.assigned_to.name : "Unassigned"}]{" "}
                    {task.completed ? (
                      <FaCheckCircle style={{ color: "green", marginLeft: "5px" }} />
                    ) : (
                      <FaTimesCircle style={{ color: "red", marginLeft: "5px" }} />
                    )}
                  </span>

                  <button onClick={() => { setEditingTask(task.id); setEditText(task.title); }} style={styles.iconButton}><FaEdit /></button>
                  <button onClick={() => handleDeleteTask(task.id)} style={styles.iconButton}><FaTrash /></button>
                  <button onClick={() => toggleComments(task.id)} style={styles.iconButton}>
                    {showComments[task.id] ? <FaEyeSlash /> : <FaEye />} Comments
                  </button>
                </>
              )}

              {/* Comments Section - Toggle Visibility */}
              {showComments[task.id] && (
                <div style={styles.commentSection}>
                  <h4>Comments</h4>
                  {task.comments.length > 0 ? (
                    <ul style={styles.commentList}>
                      {task.comments.map((comment) => (
                        <li key={comment.id} style={styles.commentItem}>
                          {editingComment[comment.id] ? (
                            <>
                              <input
                                type="text"
                                value={editCommentText}
                                onChange={(e) => setEditCommentText(e.target.value)}
                                style={styles.input}
                              />
                              <button onClick={() => handleEditComment(comment.id)} style={styles.button}>Save</button>
                              <button onClick={() => setEditingComment({})} style={styles.cancelButton}>Cancel</button>
                            </>
                          ) : (
                            <>
                              <span><strong>{comment.employee.name}:</strong> {comment.content}</span>
                              <button onClick={() => { setEditingComment({ [comment.id]: true }); setEditCommentText(comment.content); }} style={styles.iconButton}><FaEdit /></button>
                              <button onClick={() => handleDeleteComment(comment.id)} style={styles.iconButton}><FaTrash /></button>
                            </>
                          )}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No comments yet.</p>
                  )}

                  <input
                    type="text"
                    value={newComment[task.id] || ""}
                    onChange={(e) => setNewComment({ ...newComment, [task.id]: e.target.value })}
                    placeholder="Add a comment..."
                    style={styles.input}
                  />
                  <button onClick={() => handleAddComment(task.id)} style={styles.button}><FaPlus /> Add Comment</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>

      <div style={styles.column}>
        <Chatbot />
      </div>
    </div>
  );
}

const styles = {
  container: { display: "flex", gap: "20px", padding: "20px" },
  column: { flex: 1, padding: "15px", borderRadius: "8px", background: "#f0f0f5" },
  iconButton: { border: "none", background: "transparent", cursor: "pointer", fontSize: "1rem", marginLeft: "10px" },
};
