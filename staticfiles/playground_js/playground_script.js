document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll(".delete-course-btn");
  
    deleteButtons.forEach(button => {
      button.addEventListener("click", function() {
        const course_id = button.getAttribute("data-course-id");
        deleteCourse(course_id);
      });
    });
  
    function deleteCourse(course_id) {
      const csrfToken = getCookie("csrftoken");
  
      fetch(`/playground/courses/${course_id}/delete/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then(response => {
          if (response.ok) {
            location.reload();
          }
        })
        .catch(error => {
          console.error("Error:", error);
        });
    }
  
    // Function to get the CSRF token
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  

// join_course.js
document.addEventListener("DOMContentLoaded", function() {
  const joinBtn = document.getElementById("join-course-btn");
  if (joinBtn) {
    joinBtn.addEventListener("click", function() {
      const courseId = joinBtn.dataset.courseId;

      // Send an AJAX request to the Django view
      fetch(`/join-course/${courseId}/`)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert("You have successfully joined the course!");
            // Refresh the page or perform other actions as needed
          } else {
            alert("Failed to join the course.");
          }
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
  }
});
