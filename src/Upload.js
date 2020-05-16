import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Upload.css';

import {Modal, Toast, ButtonToolbar, Button, Form, Container, Row, Col} from 'react-bootstrap';



function Upload() {
  return (
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>Static Evaluation Submission</title>
</head>
<body>
<p><h1>Static Evaluation Submission</h1></p>
<form enctype="multipart/form-data" action="http://dialog.speech.cs.cmu.edu:9888/upload" method="post">
Team/Model name: <input type="text" name="filename" /> <br/> <br/>
Model outputs: <input type="file" name="file1" />
<br />
<br />
<input type="submit" value="upload" />
</form>
</body>
</html>
  );
}

export default Upload;
