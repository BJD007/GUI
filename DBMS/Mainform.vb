Imports System.Data.OleDb

Public Class MainForm
    ' Form controls declaration
    Private WithEvents btnAddRobot As New Button()
    Private WithEvents btnSearchRobot As New Button()
    Private WithEvents btnSuggestRobot As New Button()
    Private txtRobotName As New TextBox()
    Private txtRobotType As New TextBox()
    Private txtPayload As New TextBox()
    Private txtReach As New TextBox()
    Private cmbCriteria As New ComboBox()
    Private dgvRobots As New DataGridView()

    ' Database connection string
    Private connString As String = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=RobotsDB.accdb;"

    ' Form initialization
    Public Sub New()
        InitializeComponent()
    End Sub

    Private Sub InitializeComponent()
        ' Form properties
        Me.Text = "Industrial Robot Intelligent Database Management System"
        Me.Size = New Size(800, 600)

        ' Robot Name
        Me.Controls.Add(New Label() With {.Text = "Robot Name:", .Location = New Point(10, 10)})
        txtRobotName.Location = New Point(100, 10)
        txtRobotName.Size = New Size(200, 20)
        Me.Controls.Add(txtRobotName)

        ' Robot Type
        Me.Controls.Add(New Label() With {.Text = "Robot Type:", .Location = New Point(10, 40)})
        txtRobotType.Location = New Point(100, 40)
        txtRobotType.Size = New Size(200, 20)
        Me.Controls.Add(txtRobotType)

        ' Payload
        Me.Controls.Add(New Label() With {.Text = "Payload (kg):", .Location = New Point(10, 70)})
        txtPayload.Location = New Point(100, 70)
        txtPayload.Size = New Size(200, 20)
        Me.Controls.Add(txtPayload)

        ' Reach
        Me.Controls.Add(New Label() With {.Text = "Reach (mm):", .Location = New Point(10, 100)})
        txtReach.Location = New Point(100, 100)
        txtReach.Size = New Size(200, 20)
        Me.Controls.Add(txtReach)

        ' Criteria ComboBox
        Me.Controls.Add(New Label() With {.Text = "Search Criteria:", .Location = New Point(10, 130)})
        cmbCriteria.Location = New Point(100, 130)
        cmbCriteria.Size = New Size(200, 20)
        cmbCriteria.Items.AddRange(New String() {"RobotType", "Payload", "Reach"})
        Me.Controls.Add(cmbCriteria)

        ' Buttons
        btnAddRobot.Text = "Add Robot"
        btnAddRobot.Location = New Point(10, 160)
        btnAddRobot.Size = New Size(100, 30)
        Me.Controls.Add(btnAddRobot)

        btnSearchRobot.Text = "Search Robot"
        btnSearchRobot.Location = New Point(120, 160)
        btnSearchRobot.Size = New Size(100, 30)
        Me.Controls.Add(btnSearchRobot)

        btnSuggestRobot.Text = "Suggest Robot"
        btnSuggestRobot.Location = New Point(230, 160)
        btnSuggestRobot.Size = New Size(100, 30)
        Me.Controls.Add(btnSuggestRobot)

        ' DataGridView
        dgvRobots.Location = New Point(10, 200)
        dgvRobots.Size = New Size(760, 350)
        Me.Controls.Add(dgvRobots)
    End Sub

    Private Sub btnAddRobot_Click(sender As Object, e As EventArgs) Handles btnAddRobot.Click
        Try
            Using conn As New OleDbConnection(connString)
                conn.Open()
                Dim cmd As New OleDbCommand("INSERT INTO Robots (RobotName, RobotType, Payload, Reach) VALUES (?, ?, ?, ?)", conn)
                cmd.Parameters.AddWithValue("@RobotName", txtRobotName.Text)
                cmd.Parameters.AddWithValue("@RobotType", txtRobotType.Text)
                cmd.Parameters.AddWithValue("@Payload", Convert.ToDouble(txtPayload.Text))
                cmd.Parameters.AddWithValue("@Reach", Convert.ToDouble(txtReach.Text))
                cmd.ExecuteNonQuery()
                MessageBox.Show("Robot added successfully!")
                ClearInputFields()
            End Using
        Catch ex As Exception
            MessageBox.Show("Error adding robot: " & ex.Message)
        End Try
    End Sub

    Private Sub btnSearchRobot_Click(sender As Object, e As EventArgs) Handles btnSearchRobot.Click
        If cmbCriteria.SelectedIndex = -1 Then
            MessageBox.Show("Please select a search criteria.")
            Return
        End If

        Dim searchValue As String = InputBox("Enter value for " & cmbCriteria.SelectedItem)
        If String.IsNullOrEmpty(searchValue) Then Return

        Try
            Using conn As New OleDbConnection(connString)
                conn.Open()
                Dim cmd As New OleDbCommand("SELECT * FROM Robots WHERE " & cmbCriteria.SelectedItem & " = ?", conn)
                cmd.Parameters.AddWithValue("?", searchValue)
                Dim adapter As New OleDbDataAdapter(cmd)
                Dim dt As New DataTable()
                adapter.Fill(dt)
                dgvRobots.DataSource = dt
            End Using
        Catch ex As Exception
            MessageBox.Show("Error searching robots: " & ex.Message)
        End Try
    End Sub

    Private Sub btnSuggestRobot_Click(sender As Object, e As EventArgs) Handles btnSuggestRobot.Click
        Try
            Using conn As New OleDbConnection(connString)
                conn.Open()
                ' For simplicity, this example just retrieves all robots
                ' You can implement more sophisticated suggestion logic here
                Dim cmd As New OleDbCommand("SELECT * FROM Robots", conn)
                Dim adapter As New OleDbDataAdapter(cmd)
                Dim dt As New DataTable()
                adapter.Fill(dt)
                dgvRobots.DataSource = dt
                MessageBox.Show("These are all available robots. In a real system, we would implement intelligent suggestion logic here.")
            End Using
        Catch ex As Exception
            MessageBox.Show("Error suggesting robots: " & ex.Message)
        End Try
    End Sub

    Private Sub ClearInputFields()
        txtRobotName.Clear()
        txtRobotType.Clear()
        txtPayload.Clear()
        txtReach.Clear()
    End Sub
End Class
