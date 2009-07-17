(define template (list SEQUENCE (list
						(list CHOICE (list
											 (list OPTION
												 (list SEQUENCE (list
																		 (list CHOICE (list
																							  (list OPTION
																								  (list CODE "B")
																								  #f)
																							  (list OPTION
																								  (list CODE "c")
																								  #f)))
																		 (list CHOICE (list
																							  (list OPTION
																								  (list CODE "v")
																								  #f)
																							  (list OPTION
																								  (list CODE "V")
																								  #f)))))
												 #f)
											 (list OPTION
												(list SEQUENCE (list
																		(list OPTIONAL
																			(list CODE "c")
																			#f)
																		(list CODE "v")))
												#f)))
						(list CHOICE (list
											 (list OPTION
												 (list SEQUENCE (list
																		 (list CHOICE (list
																							  (list OPTION
																								  (list SEQUENCE (list
																														  (list CODE "E")
																														  (list CODE "B")))
																								  #f)
																							  (list OPTION
																								  (list CODE "B")
																								  #f)))
																		 (list CODE "v")))
												 #f)
											 (list OPTION
												 (list SEQUENCE (list
																		 (list CODE "E")
																		 (list CHOICE (list
																							  (list OPTION
																								  (list CODE "v")
																								  #f)
																							  (list OPTION
																								  (list SEQUENCE (list))
																								  #f)
																							  (list OPTION
																								  (list SEQUENCE (list))
																								  #f)
																							  (list OPTION
																								  (list SEQUENCE (list))
																								  #f)))))
												 #f)
											 (list OPTION
												 (list SEQUENCE (list
																		 (list CODE "s")
																		 (list CHOICE (list
																							  (list OPTION
																								  (list CODE "v")
																								  #f)
																							  (list OPTION
																								  (list SEQUENCE (list))
																								  #f)
																							  (list OPTION
																								  (list SEQUENCE (list))
																								  #f)
																							  (list OPTION
																								  (list SEQUENCE (list))
																								  #f)))))
												 #f)))))
)