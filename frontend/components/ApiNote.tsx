export default function ApiNote({ message }: { message: string | null }) {
  return (
    <div role="alert" className="note">
      <strong>The database service did not answer.</strong> {message ?? ''} The page itself is complete; the numbers and tables load from the API. Please try again later.
    </div>
  );
}
