from flask import Flask, render_template, request
from hw_08_ps_aux.ps_aux_parser import main as generate_report, calculate_statistics
import os

app = Flask(__name__)


# Modify index function in app.py
@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    success = None
    error_message = ""

    if request.method == 'POST':
        try:
            generate_report()
            result_file_base = max(
                [f for f in os.listdir('.') if f.endswith('-scan.csv')],
                key=lambda x: os.path.getctime(os.path.join('.', x))
            ).rsplit('.', 1)[0]
            total_cpu, total_memory, process_counter, max_cpu_name, max_cpu, max_mem_name, max_mem, users, processes_by_user, max_application_name, max_application_mem, fleet_memory_usage = calculate_statistics(
                result_file_base
            )

            filtered_processes_by_user = {user: count for user, count in processes_by_user.items() if count >= 10}

            report = [{'Category': 'System report', 'Detail': ''},
                      {'Category': 'System users', 'Detail': ', '.join(set(users))},
                      {'Category': 'Processes running', 'Detail': str(process_counter)}, {'Category': 'User processes',
                                                                                          'Detail': filtered_processes_by_user if filtered_processes_by_user else {
                                                                                              'No users with more than 10 processes.': ''}},
                      {'Category': 'Total memory used', 'Detail': f"{total_memory:.2f} MB"},
                      {'Category': 'Total CPU used', 'Detail': f"{total_cpu:.2f}"},
                      {'Category': 'Most memory used by process',
                       'Detail': f"{max_mem_name[:20]} uses {max_mem:.2f} MB"},
                      {'Category': 'Most CPU used by process', 'Detail': f"{max_cpu_name[:20]} uses {max_cpu}"},
                      {'Category': 'Application with most memory usage',
                       'Detail': f"{max_application_name[:20]} uses {max_application_mem:.2f} MB"},
                      {'Category': 'Fleet application memory usage', 'Detail': f"{fleet_memory_usage:.2f} MB"}]

            success = True

        except Exception as e:
            success = False
            error_message = str(e)
            print(f"An error occurred: {e}")

    return render_template('index.html', report=report, success=success, error_message=error_message)


# Update the template file (index.html) to include error_message for display

if __name__ == '__main__':
    app.run(debug=True)
    for f in os.listdir('.'):
        if f.endswith('-scan.csv'):
            os.remove(f)