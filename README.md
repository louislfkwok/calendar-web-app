# Calendar.io - Web App
#### Video Demo:  https://youtu.be/7_M3zWFfns0
#### Description:
Calendar.io is a web app that integrates a to-do task list and a calendar, making it easy for users to manage their events and tasks in one place.

**Technologies Used**

- Front-end: HTML, CSS, JavaScript
- Back-end: Python
- Database: SQLite

**Installation**

To run Calendar.io locally, follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/louislfkwok/calendar.git
   ```

2. Navigate to the project folder:
   ```bash
   cd calendar
   ```

3. Install the required Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Run the Flask app:
   ```bash
   flask run
   ```

**Usage**

1. Registration: If you haven't registered before, click the "Register" link in the top-right corner. Enter a unique username, password, and confirmation password to create an account.

2. Login: After successful registration, you can log in with your credentials on the login page.

3. Main Page: The main page displays your to-do list and calendar side by side.

4. To-Do List: You can add, edit, or delete tasks in the to-do list.

5. Calendar: Click on an empty slot in the calendar to add an event. The date, start time, and end time will be set automatically based on the slot you clicked. Enter the event name to add it.

6. Editing and Deleting: You can edit or delete existing tasks or events by clicking on them.

7. Error Handling: Invalid operations, such as not entering an event/task name, will redirect you to an error page (where you'll see a lovely cat!)

**Contributing**

Currently, we are not accepting contributions. Feel free to fork the project and make changes for your own use.

**License**

This project is open-source and available under the MIT License.

**Contact**

For any questions or issues, please contact Louis Kwok at louiskwok0226@gmail.com.