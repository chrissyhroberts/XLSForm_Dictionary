import pandas as pd
import argparse
import re

# Function to process grouping and path
def process_survey(survey_df, choices_df):
    group_stack = []
    path = ""
    questions = []

    # Create a mapping of variable names to labels
    name_to_label = {
    str(row['name']): str(row['label']) for _, row in survey_df.iterrows() if pd.notna(row['name']) and pd.notna(row['label'])
    }

    # Iterate over each row in the survey sheet
    for _, row in survey_df.iterrows():
        row_type = str(row.get('type', ''))  # Convert to string to handle NaN
        label = str(row['label']) if pd.notna(row.get('label')) else None
        name = str(row['name']) if pd.notna(row.get('name')) else None
        hint = str(row['hint']) if pd.notna(row.get('hint')) else None
        relevant = str(row['relevant']) if pd.notna(row.get('relevant')) else None
        constraint = str(row['constraint']) if pd.notna(row.get('constraint')) else None
        required = str(row['required']) if pd.notna(row.get('required')) else None


        # Handle group beginnings with visual bars and indentation
        if 'begin_group' in row_type or 'begin_repeat' in row_type:
            group_stack.append(label if label else name)  # Push group/repeat onto the stack

            # Calculate indentation level based on group nesting
            indent_level = len(group_stack)
            margin = 20 * indent_level  # Indentation based on group level

            # Add a visual bar for the group or repeat beginning with appropriate nesting
            if 'begin_group' in row_type:
                html_content += f"<div class='group-info' style='margin-left:{margin}px;'>Group: {name}, Label: {label}, Relevant: {relevant}</div>"
                if 'begin_repeat' in row_type:
                    html_content += f"<div class='repeat-info' style='margin-left:{margin}px;'>Repeat: {name}, Label: {label}, Relevant: {relevant}</div>"


                    if 'begin_group' in row_type:
                        group_stack.append(label if label else name)  # Use label if available



                        # Handle group endings with indentation reset

                        if 'end_group' in row_type or 'end_repeat' in row_type:
                            if group_stack:
                                group_stack.pop()  # Pop from stack to reduce indentation

                                if group_stack:
                                    group_stack.pop()  # Pop from stack to reduce indentation


                                    if 'end_group' in row_type:
                                        if group_stack:
                                            group_stack.pop()


                                            # Skip if both label and name are NaN
                                            if not label and not name:


                                                # Create the main heading: label (name)
                                                heading = label if label else ""
                                                if name:
                                                    heading += f" [{name}]" if label else name

                                                    # Replace variable names in 'relevant' with their corresponding labels and remove ${}
                                                    if relevant:
                                                        relevant = re.sub(r'\${(.*?)}', r'\1', relevant)  # Remove ${}
                                                        for var_name, var_label in name_to_label.items():
                                                            relevant = re.sub(rf"\b{var_name}\b", var_label, relevant)

                                                            # Build question structure
                                                            question_data = {
                                                            'Heading': heading,
                                                            'Name': name,
                                                            'Path': path,
                                                            'Type': row_type,
                                                            'Hint': hint,
                                                            'Relevant': relevant,
                                                            'Constraint': constraint,
                                                            'Required': required,
                                                            'Choices': None,
                                                            'Group_Level': len(group_stack),
                                                            'Group': group_stack[-1] if group_stack else None
                                                            }

                                                            # Handle select_one or select_multiple with choices
                                                            if 'select_one' in row_type or 'select_multiple' in row_type:
                                                                list_name = row_type.split()[1] if len(row_type.split()) > 1 else None
                                                                choices = choices_df[choices_df['list_name'] == list_name]
                                                                choices_list = choices['label'].tolist()
                                                                question_data['Choices'] = choices_list

                                                                questions.append(question_data)

                                                                return questions

                                                                # Function to generate HTML for each question
                                                                def generate_question_html(question):
                                                                    html = f"<div class='question-box'><h4 class='question-label'>{question['Heading']}</h4>"

                                                                    # Add additional elements with color coding
                                                                    if question['Hint']:
                                                                        html += f"<p class='hint'><strong>Hint:</strong> {question['Hint']}</p>"
                                                                        if question['Relevant']:
                                                                            html += f"<p class='relevant'><strong>Relevant:</strong> {question['Relevant']}</p>"
                                                                            if question['Constraint']:
                                                                                html += f"<p class='constraint'><strong>Constraint:</strong> {question['Constraint']}</p>"
                                                                                if question['Required']:
                                                                                    html += f"<p class='required'><strong>Required:</strong> {question['Required']}</p>"

                                                                                    # Add question type
                                                                                    html += f"<p class='type'><em>Type:</em> {question['Type']}</p>"

                                                                                    # Add choices if applicable
                                                                                    if question['Choices']:
                                                                                        html += "<ul class='choices'>"
                                                                                        for choice in question['Choices']:
                                                                                            html += f"<li>{choice}</li>"
                                                                                            html += "</ul>"

                                                                                            html += "</div>"
                                                                                            return html

                                                                                            # Function to generate HTML document
                                                                                            def save_to_html(questions, metadata, output_html):
                                                                                                # HTML Structure
                                                                                                html_content = f"""
                                                                                                <html>
                                                                                                <head>
                                                                                                <title>{metadata['Form Title']}</title>
                                                                                                <style>
                                                                                                body {{
                                                                                                font-family: 'Open Sans', sans-serif;
                                                                                                background-color: #f9f9f9;
                                                                                                color: #333;
                                                                                                }}
                                                                                                .sidebar {{
                                                                                                width: 250px;
                                                                                                float: left;
                                                                                                background-color: #2c3e50;
                                                                                                padding: 15px;
                                                                                                border-right: 1px solid #ccc;
                                                                                                height: 100%;
                                                                                                position: fixed;
                                                                                                color: white;
                                                                                                }}
                                                                                                .sidebar h2 {{
                                                                                                font-size: 20px;
                                                                                                color: #ecf0f1;
                                                                                                text-align: center;
                                                                                                margin-bottom: 20px;
                                                                                                }}
                                                                                                .sidebar ul {{
                                                                                                padding-left: 0;
                                                                                                list-style: none;
                                                                                                }}
                                                                                                .sidebar ul li {{
                                                                                                padding: 10px;
                                                                                                border-bottom: 1px solid #34495e;
                                                                                                }}
                                                                                                .sidebar ul li a {{
                                                                                                color: #ecf0f1;
                                                                                                text-decoration: none;
                                                                                                }}
                                                                                                .sidebar ul li:hover {{
                                                                                                background-color: #34495e;
                                                                                                }}
                                                                                                .content {{
                                                                                                margin-left: 270px;
                                                                                                padding: 20px;
                                                                                                }}
                                                                                                h1, h2, h3 {{
                                                                                                margin-bottom: 10px;
                                                                                                }}
                                                                                                .dropdown {{
                                                                                                cursor: pointer;
                                                                                                font-weight: bold;
                                                                                                margin-bottom: 10px;
                                                                                                background-color: #3498db;
                                                                                                color: white;
                                                                                                padding: 10px;
                                                                                                border-radius: 5px;
                                                                                                }}
                                                                                                .dropdown-content {{
                                                                                                display: block;  /* Uncollapsed by default */
                                                                                                margin-left: 20px;
                                                                                                border-left: 2px solid #ccc;
                                                                                                padding-left: 10px;
                                                                                                }}
                                                                                                .question-box {{
                                                                                                margin-bottom: 20px;
                                                                                                padding: 15px;
                                                                                                border: 1px solid #ccc;
                                                                                                border-radius: 5px;
                                                                                                background-color: white;
                                                                                                }}
                                                                                                .question-label {{
                                                                                                color: red;
                                                                                                margin-bottom: 10px;
                                                                                                }}
                                                                                                .hint {{
                                                                                                color: green;
                                                                                                }}
                                                                                                .relevant {{
                                                                                                color: blue;
                                                                                                }}
                                                                                                .constraint {{
                                                                                                color: red;
                                                                                                }}
                                                                                                .required {{
                                                                                                color: orange;
                                                                                                }}
                                                                                                .choices {{
                                                                                                margin-left: 20px;
                                                                                                }}
                                                                                                ul {{
                                                                                                list-style-type: none;
                                                                                                }}
                                                                                                ul li {{
                                                                                                padding: 5px;
                                                                                                border-bottom: 1px solid #ddd;
                                                                                                }}
                                                                                                ul li:hover {{
                                                                                                background-color: #eee;
                                                                                                }}
                                                                                                </style>
                                                                                                </head>
                                                                                                <body>
                                                                                                <div class="sidebar">
                                                                                                <h2>Groups</h2>
                                                                                                <ul>
                                                                                                """

                                                                                                # Sidebar for groups
                                                                                                groups = {}
                                                                                                for question in questions:
                                                                                                    if question['Group'] and question['Group'] not in groups:
                                                                                                        groups[question['Group']] = f"<li><a href='#{question['Group']}'>{question['Group']}</a></li>"

                                                                                                        for group in groups.values():
                                                                                                            html_content += group

                                                                                                            html_content += """
                                                                                                            </ul>
                                                                                                            </div>
                                                                                                            <div class="content">
                                                                                                            <h1>{metadata['Form Title']}</h1>
                                                                                                            <h2>ID: {metadata['Form ID']}</h2>
                                                                                                            <h2>Version: {metadata['Version']}</h2>
                                                                                                            """

                                                                                                            # Generate questions HTML with collapsible groups
                                                                                                            current_group = None
                                                                                                            for question in questions:
                                                                                                                if question['Group'] != current_group:
                                                                                                                    if current_group is not None:
                                                                                                                        html_content += "</div>"  # Close previous group's dropdown content
                                                                                                                        current_group = question['Group']
                                                                                                                        html_content += f"<div class='dropdown'>{current_group}</div>"
                                                                                                                        html_content += f"<div class='dropdown-content' id='{current_group}'>"

                                                                                                                        # Add question content
                                                                                                                        html_content += generate_question_html(question)

                                                                                                                        # Close last group
                                                                                                                        html_content += "</div>"

                                                                                                                        # Close HTML structure
                                                                                                                        html_content += """
                                                                                                                        </div>
                                                                                                                        
    <script>
        document.querySelectorAll('.choices-btn').forEach(function(button) {
            button.addEventListener('click', function() {
                const choices = this.nextElementSibling;
                if (choices.style.display === 'none' || choices.style.display === '') {
                    choices.style.display = 'block';
                    this.innerHTML = 'Hide Choices';
                } else {
                    choices.style.display = 'none';
                    this.innerHTML = 'Show Choices';
                }
            });
        });
    </script>
</body>

                                                                                                                        </html>
                                                                                                                        """

                                                                                                                        # Write to the output HTML file
                                                                                                                        with open(output_html, 'w') as file:
                                                                                                                            file.write(html_content)

                                                                                                                            def main():
                                                                                                                                # Parse the command-line argument
                                                                                                                                parser = argparse.ArgumentParser(description='Process ODK XLSX file to generate a data dictionary in HTML format with sidebar and dropdown menus.')
                                                                                                                                parser.add_argument('file', type=str, help='Path to the ODK XLSX file')
                                                                                                                                parser.add_argument('output', type=str, help='Output HTML file path')

                                                                                                                                args = parser.parse_args()

                                                                                                                                # Load the Excel file
                                                                                                                                file_path = args.file
                                                                                                                                xls = pd.ExcelFile(file_path)

                                                                                                                                # Load the relevant sheets: survey and choices
                                                                                                                                survey_df = pd.read_excel(xls, sheet_name='survey')
                                                                                                                                choices_df = pd.read_excel(xls, sheet_name='choices')
                                                                                                                                settings_df = pd.read_excel(xls, sheet_name='settings')

                                                                                                                                # Generate the list of questions with group levels
                                                                                                                                questions = process_survey(survey_df, choices_df)

                                                                                                                                # Get metadata from settings sheet
                                                                                                                                form_metadata = {
                                                                                                                                'Form Title': settings_df.loc[0, 'form_title'],
                                                                                                                                'Form ID': settings_df.loc[0, 'form_id'],
                                                                                                                                'Version': settings_df.loc[0, 'version']
                                                                                                                                }

                                                                                                                                # Save the questions to an HTML document
                                                                                                                                save_to_html(questions, form_metadata, args.output)

                                                                                                                                if __name__ == '__main__':
                                                                                                                                    main()