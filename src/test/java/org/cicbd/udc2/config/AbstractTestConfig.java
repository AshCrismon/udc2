package org.cicbd.udc2.config;

import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(
		locations = { 
				"classpath:spring/spring-mvc.xml", 
				"classpath:spring/spring-mongo.xml"  
				})
public class AbstractTestConfig {

	public void print(Object obj){
		System.out.println(obj);
	}
}
