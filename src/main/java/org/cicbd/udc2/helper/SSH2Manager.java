package org.cicbd.udc2.helper;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import ch.ethz.ssh2.Connection;
import ch.ethz.ssh2.SCPClient;
import ch.ethz.ssh2.Session;

public class SSH2Manager {

	private final static String DEFAULT_USER = "root";
	private final static String DEFAULT_PASSWORD = "000000";

	public static SSH2Client connect(String host, String user, String password)
			throws IOException {
		Connection conn = new Connection(host);
		conn.connect();
		boolean isAuthenticated = conn.authenticateWithPassword(user, password);
		if (!isAuthenticated) {
			throw new IOException("Authentication failed!");
		}
		return new SSH2Client(conn);
	}

	public static SSH2Client connect(String host) throws IOException {
		Connection conn = new Connection(host);
		conn.connect();
		boolean isAuthenticated = conn.authenticateWithPassword(DEFAULT_USER,
				DEFAULT_PASSWORD);
		if (!isAuthenticated) {
			throw new IOException("Authentication failed!");
		}
		return new SSH2Client(conn);
	}

	public static class SSH2Client {
		private Connection conn;
		private Session session;
		private SCPClient scpClient;
		private final static String QUERY_RET_CODE = "echo $?";
		private boolean lastExecuteStatus = false;

		public SSH2Client(Connection conn) throws IOException {
			this.conn = conn;
		}

		public void execCommand(String cmd) throws IOException {
			execCommand(cmd, true);
		}

		public void execCommand(String cmd, boolean printFeedback)
				throws IOException {
			if (session != null) {
				session.close(); // 每个session只能执行一次命令，每次开始执行命令时，先关闭上次的session再开启新的session
			}
			session = conn.openSession();
			session.execCommand(cmd);
			if (printFeedback) {
				printFeedback();
			}
			setLastExecuteStatus();
		}

		private void setLastExecuteStatus() throws IOException {
			if (session != null) {
				session.close();
			}
			session = conn.openSession();
			session.execCommand(QUERY_RET_CODE);
			String retCode = stdout();
			lastExecuteStatus = retCode.equals("0");
		}

		public String stdout() throws IOException {
			return feedback(session.getStdout());
		}

		public String stderr() throws IOException {
			return feedback(session.getStderr());
		}

		private String feedback(InputStream in) throws IOException {
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			StringBuilder sb = new StringBuilder();
			String output = "";
			while ((output = br.readLine()) != null) {
				sb.append(output + "\r\n");
			}
			br.close();
			String str = sb.toString();
			return str.equals("") ? str : str.substring(0,
					str.lastIndexOf("\r\n"));
		}

		private void printFeedback() throws IOException {
			print(stdout());
			print(stderr());
		}

		public void disConnect() {
			conn.close();
		}

		private void print(String result) {
			System.out.println(result);
		}

		public void put(String localFile, String remoteTargetDirectory,
				String mode) throws IOException {
			scpClient = getSCPClient();
			scpClient.put(localFile, remoteTargetDirectory, mode);
		}

		public void put(String localFile, String remoteTargetDirectory)
				throws IOException {
			put(localFile, remoteTargetDirectory, "0600");
		}

		public void putShell(String localFile, String remoteTargetDirectory)
				throws IOException {
			put(localFile, remoteTargetDirectory, "0700");
			execCommand("chmod 0700 " + remoteTargetDirectory
					+ baseFileName(localFile), false);
		}
		
		private String baseFileName(String filePath) {
			return filePath.substring(filePath.lastIndexOf("/"));
		}

		public SCPClient getSCPClient() throws IOException {
			if (scpClient == null) {
				scpClient = conn.createSCPClient();
			}
			return scpClient;
		}

		public boolean getLastExecuteStatus() {
			return lastExecuteStatus;
		}

	}

}
