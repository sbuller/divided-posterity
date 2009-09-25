(SEQUENCE (list
						(CHOICE (list
								(OPTION
									(SEQUENCE (list
											(CHOICE (list
																(OPTION (CODE B) nil)
																(OPTION (CODE c) nil)))
											(CHOICE (list
																(OPTION (CODE v) nil)
																(OPTION (CODE V) nil)))))
									nil)
								(OPTION
									(SEQUENCE (list
															(OPTIONAL (CODE c) nil) (CODE v)))
									nil)))
						(CHOICE (list
											(OPTION
												(SEQUENCE (list
																		(CHOICE (list
																							(OPTION
																								(SEQUENCE (list (CODE E) (CODE B)))
																								nil)
																							(OPTION (CODE B) nil)))
																		(CODE v)))
												nil)
											(OPTION
												(SEQUENCE (list
																		(CODE E)
																		(CHOICE (list
																							(OPTION (CODE v) nil)
																							(OPTION (SEQUENCE (list)) nil)
																							(OPTION (SEQUENCE (list)) nil)
																							(OPTION (SEQUENCE (list)) nil)))))
												nil)
											(OPTION
												(SEQUENCE (list
																		(CODE s)
																		(CHOICE (list
																							(OPTION (CODE v) nil)
																							(OPTION (SEQUENCE (list)) nil)
																							(OPTION (SEQUENCE (list)) nil)
																							(OPTION (SEQUENCE (list)) nil)))))
												nil)))))
