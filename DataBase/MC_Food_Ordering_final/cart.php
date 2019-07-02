<?php
 	include 'includes/cart.inc.php';
?>	

<!DOCTYPE html>
<html>
<head>

	<title> </title>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>

<body style="background-image:url('images/bg.jpg');">
	<header>
		<nav>
			<div class= "main-wrapper">
				<ul>
					<li><a href="index.php">MC Kitchen</a></li>
				</ul>
				<div class="nav-login">
					
					<a href="signup.php">Add Customer</a>
					<a href="deleteCustomer.php">Delete Customer</a>
					<a href="addProduct.php">Add Product</a>
					<a href="cart.php">Add Order</a>
					<a href="updateProduct.php">Update Product</a>
				</div>

			</div>
		</nav>		
	
	</header>

	<div id="main_div">
				<h3> Shopping Cart </h3>
					<div id="division">
						<section id="main_section">
							<?php display_cart(); ?>
						</section>
						<aside id="side">
							<img src="images/t.jpg" height="75" width="80"><br><br>
							<span class="your_cart">Current Items in Cart</span>&nbsp;&nbsp;
							<br><br>
							
							<?php    calculate_total(); ?>
						</aside>
					</div>
	</div>			

</body>	
</html>

					


