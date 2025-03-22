# budgetteers
Overview

    What is this project? This project we have created is a personal finance web app that people can use to track their finances. So far, our web app tracks the budget you set, the budget you set for category X, subscriptions, and any additional expenses you have, such as a cost for an emergency. We have eight files to review. They are addexpense.html, addsubscription.html, base.html, index.html, setbudget.html, setmasterbudget.html, project.py and requirements.txt.

Project Structure, Files & Functionality

    This project contains eight main files. Each of them plays a key role in both the structure and the operation of this web application program:
    addexpense.html & addsubscription.html – These templates allow users to add expenses and subscriptions. They interact with project.py to process and store the data in the database. The templates dynamically update the UI to reflect new data and alert users of upcoming subscription renewal dates.
    base.html—This file serves as the base layout for all pages, providing consistent design elements (navigation, footer, etc.) across the app. It also supports templates like addexpense.html and addsubscription.html by providing a common structure.
    index.html – The homepage where users can see an overview of their finances. It dynamically pulls data from the backend (via project.py) to show budgets, expenses, and progress on the user's financial goals. The progress bar visually represents spending against budget limits.
    setbudget.html & setmasterbudget.html – Templates where users can define both individual budgets and a master budget. These forms send user inputs to project.py, where the data is validated and stored in the database. The backend ensures that users' spending does not exceed set limits.
    project.py – The backend logic of the app, which manages routing, user input processing, and database interactions. It connects all the templates by retrieving data (such as user budgets and expenses) from the database and passing it back to the frontend templates for display. The core logic also handles calculations for remaining budget amounts and subscription due dates.
    requirements.txt—This file contains all the dependencies required to run the app, ensuring the environment is set up correctly and consistently across different machines.
    Through Flask routing, the files all work together seamlessly. "addexpense.html" is a user input template. This input is processed by project.py, which embeds logic on the back end and updates deliverables dynamically in UI pictures as it passes data from one template to another.

Design Choices

    Backend With Flask:
        We have selected Flask because it is simple and flexible, and it is also convenient for routing and form handling.
    Frontend With HTML And Bootstrap:
        HTML and Bootstrap were used not just for aesthetics but also for their ease in creating responsive, quick websites. While custom styling might provide your site with a look all of its own, Bootstrap allows for an infinitely easier way to ensure that your site will be custom no matter where it is viewed.
    Dynamic Rendering With Jinja2:
        Jinja2 was chosen for the dynamic rendering of data results and to keep updates seamless. JavaScript might have been an alternative, but Jinja2 integrates with Flask more easily, simplifying the project.
        User Input Validation:
        We did server-side validation for accurate data input. Although client-end validation was considered and discarded, there was no danger of giving server-side breakthroughs in any user environment.

Challenges and Solutions

    Challenge Data Consistency:
        We have to check that data like budgets and spending are joined together across the app journey in one place. This we achieved by centralizing the database structure and introducing checks that ensure every record fits its category one hundred percent.
    Challenge Handling User Inputs:
        Still, the idea of preventing potential input errors with our system hits home. Server-side checking of all forms is the answer: no user can ever submit unfinished or wrong data again.
    Challenge Subscription Alerts:
        With recurring subscription alerts, the dates need to be checked against current times to make judgments about when such are coming up on our hands. During the interval, there should not be any such thing as an omitted payment. To fix this, we implemented the logic of telling users before they have to put down money that their subscription is nearing its renewal date.
    Challenge Styling for Responsiveness:
        The web app needed extra attention to its platform and layout for computer users. One such bonus was Bootstrap, a package that allowed us to switch output for different screen sizes with some style changes on behalf of users themselves without further effort.

Future Improvements

    Better User Interface:
        Although the current interface functions as it does, future updates might include more vivid visuals and animations to improve user engagement and make navigation easier and less difficult.
    Mobile App Version:
        However, because the web app is not mobile-responsive yet, the actual development of a standalone mobile app may improve performance and offer exclusive features. For instance, push notifications for reminders about subscriptions nearing the renewal date.
    Advanced Reporting and Analytics:
        Detailed reports and analyses are essential to helping people understand how they spend money. Features like charts, graphs, and predictive budget analysis provide multiple benefits to this end.
    Third-Party Integrations:
        Connecting to third-party APIs means users can automatically update their bank accounts and payment processors, so there is less manual input.
    User Authentication
    Adding user authentication (e.g., login and registration) would allow users to store their financial data securely and access it across devices.

Installation & Usage

    How to Run the Project
    in your terminal, run these three commands
    pip install flask
    pip install flask_sqlalchemy
    pip install flask_migrate
    make sure that after you install each package, make sure you run the command to install the latest format of these packages
    after running these pip install commands, you can then run the simple command of python project.py

Conclusion

    After this project was successfully completed, an easy-to-use, highly efficient budgeting tool called Expense would permit one to keep a close tab on all expenditures and contracts. Through this project, we built budget allocation, progress tracking, and subscription management into the application. We also learned the necessity of full-scale user-verified input checks, responsive design, and practical background handling.
    In the future, we would like to expand the app with more advanced features like analytics, third-party integration, and even an iOS-based version. The know-how we gained from this project will help us develop even more complicated applications while keeping our attention firmly on user needs and experience.
