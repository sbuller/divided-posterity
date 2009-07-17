(define dictionary (list))
(define DEFAULT_PRIMITIVES (load "default_primitives.scm"))
  
(define (execute x)
	(apply (car x) (cdr x)))
  
(define (set name value)
(write "Set")
	(append! dictionary (list (cons name value))))
	
(define (option part not_used)
;(write "Option")
	(execute part))
	
(define (choice l)
;(write "Choice")
	(define options_explicit (list))
	(define options_residue (list))
	(define total 0)
	(for-each
		(lambda (it)
			(define percent (caddr it))
			(cond
				((integer? percent)
					(set! total (+ total percent))
					(set! options_explicit (append options_explicit (list (list it total)))))
				(else
					(set! options_residue (append options_residue (list it))))))
		l)
	(define num (random 100)) ;0<=num<100
	(define n)
	(cond
		((>= num total)
			(set! num (random (length options_residue)))
			(set! n (list-ref options_residue num)))
			(write (car n))
		(else
			(for-each
				(lambda (it)
					(if (> (cadr it) num)
						(set! n (car it))))
				options_explicit)))
		(execute n))
		
(define (sequence l . str)
;(write "Sequence")
	(if (null? l)
		(if (null? str)
			""
			(car str))
		(if (> (length str) 0)
			(sequence (cdr l) (string-append (car str) (execute (car l))))
			(sequence (cdr l) (execute (car l))))))
	
(define (optional part chance)
;(write "Optional")
	(define percent
		(if chance
			(execute chance)
			50))
	(if (< (random 100) percent)
		(execute part)
		""))
		
(define (percent num)
(write "Percent")
	num)
	
(define (var name)
(write "Var")
	(cdr (assoc name dictionary)))
	
(define (code name)
;(write "Code")
	(define n (cdr (assoc name DEFAULT_PRIMITIVES)))
	(define num (random (length n)))
	(list-ref n num))

(define (literal str)
(write "Literal")
	str)
	
(define template (load "template.scm"))

(define (gen num l)
	(if (<= num 0)
		l
		(gen (- num 1) (append l (list (execute template))))))
	
(execute template)
