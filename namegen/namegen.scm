(define dictionary (list))
(load "default_primitives.scm")

(define (execute x)
	(apply (car x) (cdr x)))

(define (SET name value)
(write "Set")
	(append! dictionary (list (cons name value))))

(define (OPTION part not_used)
;(write "Option")
	(execute part))

(define (CHOICE l)
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

(define (SEQUENCE l . str)
;(write "Sequence")
	(if (null? l)
		(if (null? str)
			""
			(car str))
		(if (> (length str) 0)
			(SEQUENCE (cdr l) (string-append (car str) (execute (car l))))
			(SEQUENCE (cdr l) (execute (car l))))))

(define (OPTIONAL part chance)
;(write "Optional")
	(define percent
		(if chance
			(execute chance)
			50))
	(if (< (random 100) percent)
		(execute part)
		""))

(define (PERCENT num)
(write "Percent")
	num)

(define (VAR name)
(write "Var")
	(cdr (assoc name dictionary)))

(define (CODE name)
;(write "Code")
	(define n (cdr (assoc name DEFAULT_PRIMITIVES)))
	(define num (random (length n)))
	(list-ref n num))

(define (LITERAL str)
(write "Literal")
	str)

(load "template.scm")

(define (gen num l)
	(if (<= num 0)
		l
		(gen (- num 1) (cons (execute template) l))))

(define (gen2 num)
	(if (not (= num 0))
		(begin
			(printf "~a\n" (execute template))
			(gen2 (- num 1)))))

(gen2 (string->number (cadr (argv))))
