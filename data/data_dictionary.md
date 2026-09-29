# Data dictionary

Each row is one synthetic video-view event. All records were generated for portfolio demonstration; no TikTok user or company data is included.

| Field | Meaning |
|---|---|
| event_id | Unique viewing event |
| event_date | Simulated event date |
| user_id | Anonymous synthetic user identifier |
| user_type | New or returning user |
| session_id | Synthetic viewing session |
| video_id | Synthetic content identifier |
| content_category | Simulated content category |
| video_length_seconds | Video duration |
| watch_time_seconds | Seconds watched, including potential rewatch time |
| watch_ratio | Watch time divided by duration |
| completed_video | 1 when at least 95% was watched |
| quick_swipe | 1 when watch time was at most 2 seconds |
| liked/shared/followed_creator/rewatched | Engagement signals |
| negative_feedback | Simulated explicit negative signal |
| continued_session | 1 if the viewer continued consuming content in the session |
