
<?php
	include_once 'header.php';
?>	


<section class="main-container">
	<div class="main-wrapper">
		<h2>Add Customer Below</h2>
		<form class ="signup-form" action= "includes/signup.inc.php" method="POST">
			<input type= "text" name="firstname" placeholder="First name">
			<br>
			<input type= "text" name="lastname" placeholder="Last name">
			<br>
			<input type= "text" name="phone" placeholder="phone number">
			<br>
			<input type= "text" name="email" placeholder="Email address">
			<br>
			<input type= "text" name="address" placeholder="Home address">
			<br>
			<input type= "text" name="username" placeholder="Username">
			<br>
			<input type= "text" name="pw" placeholder="Password">
			<br>
			<button type = "submit" name="submit">Submit</button>
	</div>
</section>	

