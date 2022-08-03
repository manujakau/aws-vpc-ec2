#!/bin/bash
sudo yum install -y httpd
ip=$(ip -o -4  address show  | awk ' NR==2 { gsub(/\/.*/, "", $4); print $4 } ')

cat <<EOF | sudo tee /var/www/html/index.html
<html>
<head>
    <title>Web App</title>
</head>
<body>
    <div style=color:black;text-align:center>
        <h1 style='font-size:7vw;'>Web App</h1>
        <p>Web app is Online.</p><small>app served from ip_address</small>
    </div>
</body>
</html>
EOF

sudo sed -i "s/ip_address/$ip/g" /var/www/html/index.html
sudo chkconfig httpd on && sudo service httpd start