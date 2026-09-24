
import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueUpdate, IssueOut, IssueStatus
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get("/")
async def get_issues():
    """Retrieve all issues."""
    issues = load_data()
    return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """Create a new issue."""
    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority.value,
        "status": IssueStatus.open
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue

@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    """Retrieve a specific issue by ID."""
    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    return issue

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    """Update an existing issue."""
    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
    # Update fields if provided
    if payload.title is not None:
        issue["title"] = payload.title
    if payload.description is not None:
        issue["description"] = payload.description
    if payload.priority is not None:
        issue["priority"] = payload.priority.value
    if payload.status is not None:
        issue["status"] = payload.status.value
    
    save_data(issues)
    return issue

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str):
    """Delete an issue by ID."""
    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
    issues.remove(issue)
    save_data(issues)
    return