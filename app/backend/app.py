from flask import Flask, jsonify, request
import boto3
import os
from datetime import datetime
import uuid
from botocore.exceptions import ClientError

app = Flask(__name__)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# AWS clients
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
env = os.getenv('ENVIRONMENT', 'dev')

# DynamoDB tables
try:
    projects_table = dynamodb.Table(f'{env}-projects')
    tasks_table = dynamodb.Table(f'{env}-tasks')
    USE_DYNAMODB = True
except:
    USE_DYNAMODB = False
    print("DynamoDB tables not found, using mock data")

@app.route('/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'dev')
    })

@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'POST':
        return create_project()
    return get_projects()

def get_projects():
    if USE_DYNAMODB:
        try:
            response = projects_table.scan()
            projects = response.get('Items', [])
            return jsonify({'projects': projects, 'source': 'dynamodb'})
        except ClientError as e:
            print(f"DynamoDB error: {e}")
    
    # Fallback to mock data
    projects = [
        {
            'project_id': '1',
            'company_id': 'demo-company',
            'name': 'Website Redesign',
            'status': 'active',
            'created_at': '2024-01-15T10:00:00Z'
        },
        {
            'project_id': '2',
            'company_id': 'demo-company', 
            'name': 'Mobile App Development',
            'status': 'planning',
            'created_at': '2024-01-20T14:30:00Z'
        }
    ]
    return jsonify({'projects': projects, 'source': 'mock'})

def create_project():
    data = request.get_json()
    project = {
        'project_id': str(uuid.uuid4()),
        'company_id': data.get('company_id', 'demo-company'),
        'name': data['name'],
        'status': data.get('status', 'planning'),
        'created_at': datetime.utcnow().isoformat()
    }
    
    if USE_DYNAMODB:
        try:
            projects_table.put_item(Item=project)
            return jsonify({'project': project, 'source': 'dynamodb'}), 201
        except ClientError as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'project': project, 'source': 'mock'}), 201

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        return create_task()
    return get_tasks()

def get_tasks():
    project_id = request.args.get('project_id')
    
    if USE_DYNAMODB:
        try:
            if project_id:
                response = tasks_table.query(
                    IndexName='project-index',
                    KeyConditionExpression='project_id = :pid',
                    ExpressionAttributeValues={':pid': project_id}
                )
            else:
                response = tasks_table.scan()
            
            tasks = response.get('Items', [])
            return jsonify({'tasks': tasks, 'source': 'dynamodb'})
        except ClientError as e:
            print(f"DynamoDB error: {e}")
    
    # Fallback to mock data
    tasks = [
        {
            'task_id': '1',
            'project_id': '1',
            'title': 'Design homepage mockup',
            'status': 'completed',
            'assignee': 'Lisa'
        },
        {
            'task_id': '2',
            'project_id': '1', 
            'title': 'Implement responsive layout',
            'status': 'in_progress',
            'assignee': 'Mike'
        }
    ]
    
    if project_id:
        tasks = [t for t in tasks if t['project_id'] == project_id]
    
    return jsonify({'tasks': tasks, 'source': 'mock'})

def create_task():
    data = request.get_json()
    task = {
        'task_id': str(uuid.uuid4()),
        'project_id': data['project_id'],
        'title': data['title'],
        'status': data.get('status', 'todo'),
        'assignee': data.get('assignee', 'unassigned'),
        'created_at': datetime.utcnow().isoformat()
    }
    
    if USE_DYNAMODB:
        try:
            tasks_table.put_item(Item=task)
            return jsonify({'task': task, 'source': 'dynamodb'}), 201
        except ClientError as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'task': task, 'source': 'mock'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)