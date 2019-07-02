
<?php
	include_once 'header.php';
?>	


<section class="main-container">
	<div class="main-wrapper">
		<h2>Add New Product Below</h2>
		<form class ="signup-form" action= "includes/addProduct.inc.php" method="POST">
			<input type= "text" name="prodID" placeholder="Product ID">
			<br>
			<input type= "text" name="prodName" placeholder="Name">
			<br>
			<input type= "text" name="description" placeholder="Description">
			<br>
			<input type= "number" step= "0.01" name="prodPrice" placeholder="Price">
			<br>
			<input type= "text" name="image" placeholder="Image URL">
			<br>
			<input type= "number" name="instock" placeholder="Quantity">
			<br>
			<input type= "text" name="catNum" placeholder="Category Number">
			<br>
			<button type = "sumbit" name="submit">Submit</button>
	</div>
</section>	

