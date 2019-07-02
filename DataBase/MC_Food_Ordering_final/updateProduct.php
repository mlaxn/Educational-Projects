
<?php
	include_once 'header.php';
?>	


<section class="main-container">
	<div class="main-wrapper">
		<h2>Update Product Below</h2>
		<form class ="signup-form" action= "includes/updateProduct.inc.php" method="POST">
			<input type= "text" name="oldName" placeholder="Original name">
			<br>
			<br>
			<input type= "text" name="newName" placeholder="New name">
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
			<button type = "sumbit" name="submit">Update Product</button>
	</div>
</section>	

