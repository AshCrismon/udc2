package org.cicbd.udc2.service;

import java.io.IOException;

public interface GangliaService {

	void installAgent(String host, String user, String password) throws IOException;
	void installServer(String host, String user, String password) throws IOException;
	void installSinker(String host, String user, String password) throws IOException;
}
