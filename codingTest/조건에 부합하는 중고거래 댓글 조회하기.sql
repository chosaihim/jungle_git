# 게시글 제목, 게시글 ID, 댓글 ID, 댓글 작성자 ID, 댓글 내용, 댓글 작성일
SELECT b.TITLE, b.BOARD_ID, r.REPLY_ID, r.WRITER_ID, r.CONTENTS, substr(r.CREATED_DATE,1,10)
FROM USED_GOODS_BOARD b, USED_GOODS_REPLY r
WHERE b.BOARD_ID = r.BOARD_ID
AND YEAR(b.CREATED_DATE) = 2022
AND MONTH(b.CREATED_DATE) = 10
ORDER BY r.CREATED_DATE, b.TITLE


-- https://school.programmers.co.kr/learn/courses/30/lessons/164673