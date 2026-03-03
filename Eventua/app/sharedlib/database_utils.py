from app.database.connection import get_connection

def get_eventID(eventName, eventYear, username):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Retrieve event_id (works for both insert and update) 
            cursor.execute( 
                "SELECT eventID FROM events WHERE eventName=? AND eventYear=? AND created_by=?", 
                (eventName, eventYear, username) 
            ) 
            
            eventID = cursor.fetchone()[0] 
            return eventID
            
    except Exception as e:
        print("Database error:", e)
        raise HTTPException(status_code=500, detail=f"Database save failed: {e}")

