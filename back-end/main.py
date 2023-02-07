from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/tasks',methods=["GET"])
def task_list():
    con = sqlite3.connect("taskdb.db")
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM tasks
    """)
   
    out = cur.fetchall()
    return {
      "data": out,
      "size": len(out),
      "ok": True
    }

@app.route('/tasks/<id>')
def task_details(id):
    con = sqlite3.connect("taskdb.db")
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM tasks WHERE id = ?
    """, (id,))
   
    out = cur.fetchall()
    return {
      "data": out,
      "size": len(out),
      "ok": True
    }

@app.route('/tasks',methods=["PUT"])
def insr_task():
    con = sqlite3.connect("taskdb.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO tasks(id, content) VALUES(?,?)
    """, (request.json["id"],request.json["content"]))
    con.commit()
    return {
      "ok": True
    }

@app.route('/tasks/<id>',methods=["DELETE"])
def del_task(id):
    con = sqlite3.connect("taskdb.db")
    cur = con.cursor()
    cur.execute("""
    DELETE FROM tasks WHERE id = ?
    """, (id,))
    con.commit()
    return {
      "ok": True
    }

@app.route('/tasks/<id>',methods=["PATCH"])
def pat_task(id):
    con = sqlite3.connect("taskdb.db")
    cur = con.cursor()
    cur.execute("""
    UPDATE tasks SET done = ?, content = ?  WHERE id = ?
    """, (request.json["done"],request.json["content"], id))
    con.commit()
    return {
      "ok": True
    }

app.run(host='0.0.0.0', port=81)