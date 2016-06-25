package org.cicbd.udc2.config;

import java.util.Iterator;

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

	public void print(String remark){
		System.out.println(";;;;;;;;;;;;;;;;;;;;;;;;" + remark + ";;;;;;;;;;;;;;;;;;;;;;;;");
	}
	
	public void print(Object result){
		System.out.println(result);
	}
	
	public void print(Iterable<?> itr){
		Iterator<?> it = itr.iterator();
		while(it.hasNext()){
			System.out.println(it.next().toString());
		}
	}
}
