; LLVM IR gerado para linguagem LSD
; Target: x86-64

target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc"

declare i32 @printf(i8*, ...)

define i32 @main() {
entry:
  %0 = fadd double 0.000000e+00, 8.500000e+00
  %1 = alloca double, align 8
  store double %0, double* %1, align 8
  %2 = fadd double 0.000000e+00, 7.000000e+00
  %3 = alloca double, align 8
  store double %2, double* %3, align 8
  %4 = load double, double* %1, align 8
  %5 = load double, double* %3, align 8
  %6 = fadd double %4, %5
  %7 = alloca double, align 8
  store double %6, double* %7, align 8
  %8 = load double, double* %7, align 8
  %9 = sitofp i32 2 to double
  %10 = fdiv double %8, %9
  %11 = alloca double, align 8
  store double %10, double* %11, align 8
  %12 = load double, double* %11, align 8
  %13 = fadd double 0.000000e+00, 7.000000e+00
  %14 = fcmp oge double %12, %13
  %15 = uitofp i1 %14 to double
  %16 = fcmp one double %15, 0.000000e+00
  br i1 %16, label %if0, label %end1

if0:
  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @str.0, i64 0, i64 0))
  %17 = load double, double* %11, align 8
  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.1, i64 0, i64 0), double %17)
  br label %end1

end1:
  ret i32 0
}

@str.0 = private unnamed_addr constant [9 x i8] c"Aprovado\00"

@str.1 = private unnamed_addr constant [4 x i8] c"%f\0A\00"
