
<?php
	include_once 'header.php';
?>	


<section class="main-container">
	<div class="main-wrapper">
		<h2>Delete Customer Below</h2>
		<form class ="signup-form" action= "includes/deleteCustomer.inc.php" method="POST">
			<input type= "text" name="firstname" placeholder="First name">
			<br>
			<input type= "text" name="lastname" placeholder="Last name">
			<button type = "sumbit" name="submit">Delete</button>
	</div>
</section>	

