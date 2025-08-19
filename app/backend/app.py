from flask import Flask, jsonify, request
import boto3
import os
from datetime import datetime

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

@app.route('/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'dev')
    })

@app.route('/api/projects', methods=['GET'])
def get_projects():
    # Mock data for dev environment
    projects = [
        {
            'id': '1',
            'name': 'Website Redesign',
            'status': 'active',
            'created_at': '2024-01-15T10:00:00Z'
        },
        {
            'id': '2', 
            'name': 'Mobile App Development',
            'status': 'planning',
            'created_at': '2024-01-20T14:30:00Z'
        }
    ]
    return jsonify({'projects': projects})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    project_id = request.args.get('project_id')
    # Mock data for dev environment
    tasks = [
        {
            'id': '1',
            'project_id': '1',
            'title': 'Design homepage mockup',
            'status': 'completed',
            'assignee': 'Lisa'
        },
        {
            'id': '2',
            'project_id': '1', 
            'title': 'Implement responsive layout',
            'status': 'in_progress',
            'assignee': 'Mike'
        }
    ]
    
    if project_id:
        tasks = [t for t in tasks if t['project_id'] == project_id]
    
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)