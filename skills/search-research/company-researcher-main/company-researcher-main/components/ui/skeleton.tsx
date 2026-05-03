import { cn } from "@/lib/utils"

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "animate-pulse rounded-md bg-secondary-darkest",
        className
      )}
      style={{
        backgroundColor: 'var(--secondary-darkest)'
      }}
      {...props}
    />
  )
}

export { Skeleton } 