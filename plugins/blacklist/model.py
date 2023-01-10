from utils.db import db_query


class BlacklistModel:
    @staticmethod
    async def add_black_user(qid):
        sql = F"""
            INSERT INTO bot.black_list (qid) VALUES ({qid});
        """
        return await db_query(sql)

    @staticmethod
    async def query_user(qid):
        sql = F"""
            SELECT * FROM bot.black_list WHERE qid={qid}
        """
        return await db_query(sql)

    @staticmethod
    async def all():
        sql = F"""
            SELECT qid FROM bot.black_list;
        """

        return await db_query(sql)

    @staticmethod
    async def delete(qid):
        sql = F"""
            DELETE FROM bot.black_list WHERE qid={qid}
        """
        return await db_query(sql)
