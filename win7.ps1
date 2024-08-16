Add-Type -AssemblyName System.Windows.Forms

# 创建一个新的窗口
$form = New-Object System.Windows.Forms.Form
$form.Text = "IP地址更改器"
$form.Size = New-Object System.Drawing.Size(300, 150)
$form.StartPosition = "CenterScreen"

# 标签显示当前 IP 地址
$label = New-Object System.Windows.Forms.Label
$label.Text = "当前 IP 地址: "
$label.AutoSize = $true
$label.Location = New-Object System.Drawing.Point(10, 20)
$form.Controls.Add($label)

# 文本框用于输入新的 IP 地址的最后一部分
$textBoxIP = New-Object System.Windows.Forms.TextBox
$textBoxIP.Location = New-Object System.Drawing.Point(10, 50)
$form.Controls.Add($textBoxIP)

# 按钮用于提交新的 IP 地址
$button = New-Object System.Windows.Forms.Button
$button.Text = "更改 IP"
$button.Location = New-Object System.Drawing.Point(10, 80)
$form.Controls.Add($button)

# 获取当前 IP 并显示在窗口中
$adapter = Get-WmiObject -Query "SELECT * FROM Win32_NetworkAdapter WHERE NetConnectionStatus=2"
$ipConfig = Get-WmiObject -Query "SELECT * FROM Win32_NetworkAdapterConfiguration WHERE InterfaceIndex=$($adapter.InterfaceIndex) AND IPEnabled=TRUE"
$currentIP = $ipConfig.IPAddress[0]
$label.Text += $currentIP

# 按钮点击事件
$button.Add_Click({
    $newIPLastOctet = $textBoxIP.Text
    $newIP = "10.2.91.$newIPLastOctet"
    $ipConfig.EnableStatic($newIP, "255.255.255.0")
    $ipConfig.SetGateways("10.2.91.1")

    # 设置固定 DNS 服务器
    $dnsServers = "10.2.91.254","10.2.2.2"
    $ipConfig.SetDNSServerSearchOrder($dnsServers)

    [System.Windows.Forms.MessageBox]::Show("IP 地址已更改为: $newIP", "操作成功")
    $form.Close()
})

# 显示窗口
$form.ShowDialog()
