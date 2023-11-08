using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Socket
{
    public partial class Form1 : Form
    {
        public class Client
        {
            public void StartClient()
            {
                void Main(string[] args)
                {
                    TcpListener server = null;
                    try
                    {
                        // Set the TcpListener on port 9999.
                        Int32 port = 9999;
                        IPAddress localAddr = IPAddress.Parse("127.0.0.1");

                        // TcpListener server = new TcpListener(port);
                        server = new TcpListener(localAddr, port);

                        // Start listening for client requests.
                        server.Start();

                        // Buffer for reading data
                        Byte[] bytes = new Byte[256];
                        String data = null;

                        // Enter the listening loop.
                        while (true)
                        {
                            Console.Write("Waiting for a connection... ");

                            // Perform a blocking call to accept requests.
                            TcpClient client = server.AcceptTcpClient();
                            Console.WriteLine("Connected!");

                            data = null;

                            // Get a stream object for reading and writing
                            NetworkStream stream = client.GetStream();

                            int i;

                            // Loop to receive all the data sent by the client.
                            while ((i = stream.Read(bytes, 0, bytes.Length)) != 0)
                            {
                                // Translate data bytes to a ASCII string.
                                data = Encoding.ASCII.GetString(bytes, 0, i);
                                Console.WriteLine("Received: {0}", data);

                                // Process the data sent by the client.
                                data = data.ToUpper();

                                byte[] msg = Encoding.ASCII.GetBytes(data);

                                // Send back a response.
                                stream.Write(msg, 0, msg.Length);
                                Console.WriteLine("Sent: {0}", data);

                                // Here you would add code to perform actions based on the gesture received.
                                // This is where you would trigger GUI actions or other operations in response to gestures.
                            }

                            // Shutdown and end connection
                            client.Close();
                        }
                    }
                    catch (SocketException e)
                    {
                        Console.WriteLine("SocketException: {0}", e);
                    }
                    finally
                    {
                        // Stop listening for new clients.
                        server?.Stop();
                    }

                    Console.WriteLine("\nHit enter to continue...");
                    Console.Read();
                }
            }

            int Main(String[] args)
            {
                Client client = new Client();
                client.StartClient();
                return 0;
            }
        }
        public Form1()
        {
            InitializeComponent();
        }
    }
}
