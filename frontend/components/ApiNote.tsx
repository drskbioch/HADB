export default function ApiNote({ message }: { message: string | null }) {
  return (
    <div role="alert" className="note">
      <strong>Data could not be loaded.</strong> {message ?? ''}
    </div>
  );
}
