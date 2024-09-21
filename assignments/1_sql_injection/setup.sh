
sudo usermod -aG docker $USER && newgrp docker && sudo systemctl start docker