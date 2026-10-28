"""Focused checks for exposure counts, review ranking, and grammar notes."""

import json
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

import server


class TrainingSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_db = server.DB
        server.DB = Path(self.temp.name) / "practice.sqlite3"
        server.database().close()

    def tearDown(self):
        server.DB = self.original_db
        self.temp.cleanup()

    def test_unseen_sentences_precede_repeats_in_each_mode(self):
        pool = server.LIST_PHRASES["N4"]["youtube:cy9P8f4lrEw"]
        picks = [server.next_phrase("N4", "Listening", "youtube:cy9P8f4lrEw") for _ in pool]
        self.assertEqual(len({phrase["id"] for phrase,count in picks}),len(pool))
        self.assertTrue(all(count == 1 for phrase,count in picks))
        self.assertEqual(server.next_phrase("N4", "Listening", "youtube:cy9P8f4lrEw")[1],2)
        self.assertEqual(server.next_phrase("N4", "Writing", "youtube:cy9P8f4lrEw")[1],1)
        for _ in range(20):
            phrase,_ = server.next_phrase("N5","Writing","main")
            self.assertGreaterEqual(len(phrase["tokens"]),3)

    def test_review_includes_unscored_saved_cards_and_persists_ratings(self):
        with server.database() as con:
            for index in range(25):
                word = f"語{index}"
                con.execute("""INSERT INTO review_saved(level,item_key,kind,text,reading,meaning)
                    VALUES(?,?,?,?,?,?)""", ("N4",server.review_key("word",word),"word",word,"ご","palavra"))
            con.execute("""INSERT INTO review_saved(level,item_key,kind,text,reading,meaning)
                VALUES(?,?,?,?,?,?)""", ("N3",server.review_key("word","語0"),"word","語0","ご","palavra"))
        self.assertEqual(len(server.review_cards("N4")),25)
        key = server.review_key("word","語0")
        http = server.LocalHTTPServer(("127.0.0.1",0),server.Handler)
        worker = threading.Thread(target=http.serve_forever,daemon=True)
        worker.start()
        try:
            url = f"http://127.0.0.1:{http.server_port}/api/review/rate"
            for rating,expected in (("easy",1),("hard",0),("hard",-1)):
                body = json.dumps({"level":"N3","key":key,"rating":rating}).encode()
                request = urllib.request.Request(url,body,{"Content-Type":"application/json"})
                with urllib.request.urlopen(request) as response:
                    result = json.load(response)
                self.assertEqual(result["points"],expected)
            rated = next(card for card in server.review_cards("N3") if card["key"] == key)
            self.assertEqual(rated["points"],-1)
            self.assertFalse(rated["unscored"])
        finally:
            http.shutdown()
            http.server_close()
            worker.join(timeout=2)

    def test_video_grammar_is_specific_and_explains_formation(self):
        phrase = server.PHRASES[2544]
        details = server.grammar_details(phrase)
        self.assertGreaterEqual(len(details),2)
        self.assertNotIn("legenda de vídeo",[item["title"] for item in details])
        self.assertTrue(all(item["meaning_pt"] and item["formation_pt"] for item in details))
        http = server.LocalHTTPServer(("127.0.0.1",0),server.Handler)
        worker = threading.Thread(target=http.serve_forever,daemon=True)
        worker.start()
        try:
            url = f"http://127.0.0.1:{http.server_port}/api/submit"
            body = json.dumps({"id":phrase["id"],"text":phrase["text"]},ensure_ascii=False).encode()
            request = urllib.request.Request(url,body,{"Content-Type":"application/json"})
            with urllib.request.urlopen(request) as response:
                result = json.load(response)
            self.assertEqual(result["correct"],result["total"])
            self.assertEqual(result["grammar_details"],details)
        finally:
            http.shutdown()
            http.server_close()
            worker.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
