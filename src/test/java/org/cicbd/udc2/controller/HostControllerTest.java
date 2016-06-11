package org.cicbd.udc2.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.webAppContextSetup;

import org.cicbd.udc2.config.AbstractTestConfig;
import org.junit.Before;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.web.context.WebApplicationContext;

import static org.junit.Assert.*;

@WebAppConfiguration
public class HostControllerTest extends AbstractTestConfig {

	@Autowired
	private WebApplicationContext wac;
	private MockMvc mockMvc;

	@Before
	public void setup() throws Exception {
		mockMvc = webAppContextSetup(wac).build();
		assertNotNull(mockMvc);
	}

	@Test
	public void testFindMetricData() throws Exception {
		mockMvc.perform(get("/metric/ganglia.cloudserver/cpu_idle?beginTime=1460713845&endTime=1460723845").accept(MediaType.APPLICATION_JSON))
				.andExpect(status().isOk())
				.andDo(MockMvcResultHandlers.print());
	}

}
