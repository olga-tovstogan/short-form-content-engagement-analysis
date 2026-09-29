-- Product engagement analysis (PostgreSQL-compatible)
-- Assumes synthetic_user_events is loaded as a table with the same name.

-- 1. Category scorecard: normalize watch time by duration.
SELECT content_category,
       COUNT(*) AS views,
       ROUND(AVG(watch_time_seconds), 2) AS avg_watch_seconds,
       ROUND(AVG(watch_ratio), 3) AS avg_watch_ratio,
       ROUND(AVG(completed_video), 3) AS completion_rate,
       ROUND(AVG(quick_swipe), 3) AS quick_swipe_rate,
       ROUND(AVG(shared), 3) AS share_rate,
       ROUND(AVG(followed_creator), 3) AS follow_rate,
       ROUND(AVG(continued_session), 3) AS continuation_rate
FROM synthetic_user_events
GROUP BY content_category
ORDER BY avg_watch_ratio DESC;

-- 2. Compare new and returning users.
SELECT user_type, content_category,
       COUNT(*) AS views,
       AVG(watch_ratio) AS avg_watch_ratio,
       AVG(completed_video) AS completion_rate,
       AVG(continued_session) AS continuation_rate
FROM synthetic_user_events
GROUP BY user_type, content_category
ORDER BY user_type, continuation_rate DESC;

-- 3. Detect content with attention but weak downstream intent.
SELECT video_id, content_category, COUNT(*) AS views,
       AVG(watch_ratio) AS avg_watch_ratio,
       AVG(shared) AS share_rate,
       AVG(followed_creator) AS follow_rate,
       AVG(negative_feedback) AS negative_feedback_rate
FROM synthetic_user_events
GROUP BY video_id, content_category
HAVING COUNT(*) >= 10 AND AVG(watch_ratio) >= 0.70
ORDER BY negative_feedback_rate DESC, share_rate ASC;
