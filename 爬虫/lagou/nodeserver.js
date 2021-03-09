const express = require('express')
const fs = require('fs')

const app = express()

app.get('/lagou', (req, res) => {
  fname = req.query.name
  seed = req.query.seed
  ts = req.query.ts
  console.log(req.query)
  qcontent = "?seed="+seed+"&ts="+ts+"&name="+fname;
  txt = fs.readFileSync(fname+'.js').toString()
  var window ={}; 
  window['location']={hostname:'www.lagou.com',search:qcontent}
  eval(txt)
  var ab = window['gt'];
  c = (new ab()).a()
  res.send(c)
});
